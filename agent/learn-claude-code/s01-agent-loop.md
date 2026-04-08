# s01 - Agent Loop（Agent 循环）

`[ s01 ] s02 > s03 > s04 > s05 > s06 | s07 > s08 > s09 > s10 > s11 > s12`

> **核心格言**：*"One loop & Bash is all you need"* -- 一个工具 + 一个循环 = 一个 Agent。

---

## 问题

LLM 很聪明，但碰不到真实世界。它不能读文件、跑命令、查数据库。你问它"项目里有哪些文件"，它只能猜。没有循环的话，每次工具调用你都得手动把结果粘回去 -- 你自己就是那个循环，人肉中间件。

Agent 的本质就是把这个"人肉中间件"自动化。

---

## Agent 的三个角色

```
+----------+      +-------+      +---------+
|   User   | ---> |  LLM  | ---> |  Tool   |
|  提需求  |      | AI大脑 |      |  干活   |
+----------+      +---+---+      +----+----+
                      ^               |
                      |   tool_result |
                      +---------------+
                      (循环继续)
```

| 角色 | 谁 | 干什么 |
|------|-----|--------|
| **用户** | 人 | 提需求："帮我列出当前目录的文件" |
| **AI 大脑** | LLM | 做决策：应该调用 `bash` 工具跑 `ls` |
| **工具** | 代码执行器 | 干活：真正执行 `ls`，拿到结果 |

核心洞察：**AI 是司机，代码是车。代码不决定去哪里，AI 决定。代码只负责执行命令、收集结果、喂回给 AI。**

---

## 核心机制：ReAct 循环

这个循环模式学术上叫 **ReAct**（Reasoning + Acting + Observation）：

1. **Reasoning** -- LLM 思考应该做什么
2. **Acting** -- LLM 调用工具
3. **Observation** -- 工具结果喂回给 LLM

代码实现极其简洁：

```python
while stop_reason == "tool_use":
    response = LLM(messages, tools)
    execute tools
    append results
```

退出条件只有一个：`stop_reason != "tool_use"` -- 当 AI 觉得不需要再调用工具时，循环结束。

---

## 代码详解

完整代码在 `agents/s01_agent_loop.py`，不到 120 行。下面逐段解释。

### 第 1 段：准备工作

```python
import os
import subprocess

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv(override=True)

if os.getenv("ANTHROPIC_BASE_URL"):
    os.environ.pop("ANTHROPIC_AUTH_TOKEN", None)

client = Anthropic(base_url=os.getenv("ANTHROPIC_BASE_URL"))
MODEL = os.environ["MODEL_ID"]
```

要点：
- `load_dotenv` 从 `.env` 文件加载环境变量
- `Anthropic` 客户端接受 `base_url` 参数 -- 这意味着**任何兼容 Anthropic API 格式的服务都能用**（OpenRouter、本地 Ollama、自建代理等），不锁死在 Anthropic 官方 API
- `MODEL_ID` 从环境变量读取，不硬编码模型名

### 第 2 段：System Prompt

```python
SYSTEM = f"You are a coding agent at {os.getcwd()}. Use bash to solve tasks. Act, don't explain."
```

System prompt 是给 AI 的**人设指令**。这里有三个关键设计：
- 告诉 AI 当前工作目录（`os.getcwd()`），让它知道自己在哪
- 明确告诉它用 bash 来干活
- **"Act, don't explain"** 是最关键的一句 -- 没有这句话，AI 会长篇大论解释它打算做什么，而不是直接动手。这句话把"话痨顾问"变成"动手型执行者"

### 第 3 段：工具定义（TOOLS）

```python
TOOLS = [{
    "name": "bash",
    "description": "Run a shell command.",
    "input_schema": {
        "type": "object",
        "properties": {"command": {"type": "string"}},
        "required": ["command"],
    },
}]
```

这是**工具的说明书**，用 JSON Schema 格式描述。AI 读这个来决定：
- 有哪些工具可用（这里只有 `bash`）
- 每个工具接受什么参数（`command`，字符串类型）
- 哪些参数必填（`required`）

AI 不是"调用函数"，它是**生成一段 JSON**，描述它想调用什么工具、传什么参数。我们的代码负责解析这段 JSON 并真正执行。

### 第 4 段：工具执行函数

```python
def run_bash(command: str) -> str:
    # Safety check
    dangerous = ["rm -rf /", "sudo", "shutdown", "reboot", "> /dev/"]
    if any(d in command for d in dangerous):
        return "Error: Dangerous command blocked"
    try:
        r = subprocess.run(command, shell=True, cwd=os.getcwd(),
                           capture_output=True, text=True, timeout=120)
        out = (r.stdout + r.stderr).strip()
        return out[:50000] if out else "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: Timeout (120s)"
```

执行流程：
1. **安全检查** -- 黑名单过滤危险命令（`rm -rf /`、`sudo` 等）
2. **subprocess 执行** -- 用 `subprocess.run` 真正跑 shell 命令，`capture_output=True` 捕获 stdout 和 stderr
3. **截取输出** -- 最多返回 50000 字符（防止巨量输出撑爆上下文窗口）
4. **超时保护** -- 120 秒超时，防止死循环命令卡住

注意：错误也返回字符串，不抛异常。这样 AI 能看到错误信息并自行纠正。

### 第 5 段：核心循环（agent_loop）

```python
def agent_loop(messages: list):
    while True:
        # Step 1: Send messages + tools to LLM
        response = client.messages.create(
            model=MODEL, system=SYSTEM, messages=messages,
            tools=TOOLS, max_tokens=8000,
        )
        # Step 2: Append assistant response to history
        messages.append({"role": "assistant", "content": response.content})

        # Step 3: Check stop_reason -- if not tool_use, we're done
        if response.stop_reason != "tool_use":
            return

        # Step 4: Execute each tool call, collect results
        results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"\033[33m$ {block.input['command']}\033[0m")
                output = run_bash(block.input["command"])
                print(output[:200])
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                })

        # Step 5: Tool results go back as a "user" message
        messages.append({"role": "user", "content": results})
        # Loop back to Step 1
```

这是整个 agent 的心脏。每轮循环做 5 件事：

1. 把**完整消息历史** + **工具定义**发给 LLM
2. 把 LLM 的回复追加到 `messages` 列表
3. 检查 `stop_reason` -- 如果 AI 没有调用工具，说明它已经有了最终答案，退出循环
4. 遍历 AI 回复中的工具调用块（`block.type == "tool_use"`），逐个执行
5. 把所有工具结果打包成一条 `user` 消息追加到 `messages` -- 然后回到第 1 步

---

## messages 列表是累积的

`messages` 列表**从不清空**，每轮都在追加。这意味着 AI 能看到：
- 用户的原始提问
- 自己之前的所有回复
- 所有工具调用和返回结果
- 上一轮的错误信息（如果有的话）

这就是 AI 能"记住上下文"的原因 -- 不是 AI 真的有记忆，而是我们每次都把完整对话历史重新喂给它。

---

## 完整流程举例

用户问："列出当前目录的文件"

```
Round 1:
  messages = [
    {role: "user", content: "列出当前目录的文件"}
  ]
  → LLM 回复: 调用 bash 工具, command="ls -la"
  → stop_reason = "tool_use"

  执行 ls -la → 得到文件列表

  messages = [
    {role: "user", content: "列出当前目录的文件"},
    {role: "assistant", content: [tool_use(bash, "ls -la")]},
    {role: "user", content: [tool_result("README.md\nagents/\n...")]}
  ]

Round 2:
  → LLM 看到 ls 结果, 生成总结回答
  → stop_reason = "end_turn" (不是 tool_use)
  → 循环结束
```

两轮就完成了。如果任务更复杂，AI 可能连续调用十几轮工具 -- 循环会自动持续，直到 AI 自己决定停下来。

---

## 关键洞察

| 概念 | 解释 |
|------|------|
| AI 是司机，代码是车 | 代码不决定去哪里，AI 决定。代码只负责执行、收集结果、喂回去 |
| 退出条件在 AI 手里 | `stop_reason` 由 AI 决定，不是代码硬编码的 |
| messages 是状态 | 整个 agent 的"记忆"就是 `messages` 列表 |
| 工具结果伪装成 user 消息 | API 协议要求工具结果以 `user` 角色发送 |
| 30 行代码 | 去掉样板代码，核心循环不到 30 行 -- 后面 11 个 session 都在这个循环上叠加机制 |

这个循环模式就是 **ReAct**（Reasoning + Acting + Observation）。2022 年 Yao et al. 提出，现在是几乎所有 AI agent 框架的基础。理解了这 30 行，你就理解了 Claude Code、Cursor、Windsurf 等产品背后的核心引擎。
