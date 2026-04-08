# s04 - Subagent（子 Agent）

`s01 > s02 > s03 > [ s04 ] s05 > s06 | s07 > s08 > s09 > s10 > s11 > s12`

> **核心格言**：*"大任务拆小，每个小任务干净的上下文"* -- 子 agent 用完即扔，主 agent 头脑清醒。

---

## 问题

messages 列表**只增不减**。AI 读了 30 个文件、跑了 20 条命令，所有中间输出永久留在上下文里。到第 50 轮的时候，messages 里 90% 是过期的工具输出，AI 的注意力被严重稀释 -- 第 1 轮读的文件内容还在那里占位置，但早就没用了。

类比：**老板亲自翻箱倒柜**找一份文件。翻的过程中桌上堆满了不相关的东西，最后连自己要找什么都忘了。

更好的做法：**叫小弟去查**。小弟自己翻箱倒柜，回来只说一句话："那份合同在第三个柜子里，金额是 50 万。" 老板桌上干干净净。

---

## 解决方案：task 工具 + 子 Agent

主 agent 拥有一个特殊工具 `task`。调用时，启动一个**全新的子 agent**：

```
Parent agent                     Subagent
+------------------+             +------------------+
| messages=[...]   |             | messages=[]      |  <-- 全新，干净
|                  |  dispatch   |                  |
| tool: task       | ---------->| while tool_use:  |
|   prompt="..."   |            |   call tools     |
|                  |            |   append results |
|                  |  summary   |                  |
|   result = "..." | <--------- | return last text |
+------------------+             +------------------+
          |
Parent context stays clean.
Subagent context is discarded.
```

---

## 子 Agent 三个关键设计

### 1. `sub_messages = []` -- 全新消息列表

```python
def run_subagent(prompt: str) -> str:
    sub_messages = [{"role": "user", "content": prompt}]  # fresh context
```

子 agent 看不到主 agent 的任何历史。它只知道一件事：主 agent 交代的任务（`prompt`）。干净的上下文意味着**100% 的注意力都在当前任务上**。

### 2. 没有 `task` 工具 -- 防止无限递归

```python
# Child gets all base tools except task (no recursive spawning)
CHILD_TOOLS = [
    {"name": "bash", ...},
    {"name": "read_file", ...},
    {"name": "write_file", ...},
    {"name": "edit_file", ...},
]
```

子 agent 能用所有基础工具（bash、读文件、写文件、编辑文件），但**没有 task 工具**。也就是说子 agent 不能再生子 agent -- 防止无限递归。

### 3. 只返回最终文本摘要 -- 中间过程全部丢弃

```python
# Only the final text returns to the parent -- child context is discarded
return "".join(b.text for b in response.content if hasattr(b, "text")) or "(no summary)"
```

子 agent 可能读了 10 个文件、跑了 5 条命令，但回给主 agent 的只有一段文本摘要。`sub_messages` 列表连同所有中间结果一起被 Python 垃圾回收。

---

## PARENT_TOOLS 和 CHILD_TOOLS 的关系

```python
PARENT_TOOLS = CHILD_TOOLS + [
    {"name": "task",
     "description": "Spawn a subagent with fresh context. It shares the filesystem but not conversation history.",
     "input_schema": {
         "type": "object",
         "properties": {
             "prompt": {"type": "string"},
             "description": {"type": "string", "description": "Short description of the task"}
         },
         "required": ["prompt"]
     }},
]
```

一行代码说清了关系：**父工具 = 子工具 + task**。子 agent 和主 agent 的唯一区别就是有没有 `task` 工具。其他完全一样 -- 一样的循环、一样的基础工具、一样的 dispatch map。

---

## run_subagent() -- 就是 s01 的循环

```python
def run_subagent(prompt: str) -> str:
    sub_messages = [{"role": "user", "content": prompt}]
    for _ in range(30):  # safety limit
        response = client.messages.create(
            model=MODEL, system=SUBAGENT_SYSTEM, messages=sub_messages,
            tools=CHILD_TOOLS, max_tokens=8000,
        )
        sub_messages.append({"role": "assistant", "content": response.content})
        if response.stop_reason != "tool_use":
            break
        results = []
        for block in response.content:
            if block.type == "tool_use":
                handler = TOOL_HANDLERS.get(block.name)
                output = handler(**block.input) if handler else f"Unknown tool: {block.name}"
                results.append({"type": "tool_result", "tool_use_id": block.id, "content": str(output)[:50000]})
        sub_messages.append({"role": "user", "content": results})
    return "".join(b.text for b in response.content if hasattr(b, "text")) or "(no summary)"
```

仔细看 -- 这就是 s01 的 agent_loop，只有两处不同：

1. `for _ in range(30)` -- 最多 30 轮，安全限制防止子 agent 失控
2. 最后 `return` 文本摘要，而不是直接输出

System prompt 也不同：`SUBAGENT_SYSTEM` 告诉子 agent "完成任务后总结发现"，引导它在结束时生成有用的摘要。

---

## 主循环中 task 的特殊处理

```python
for block in response.content:
    if block.type == "tool_use":
        if block.name == "task":
            desc = block.input.get("description", "subtask")
            print(f"> task ({desc}): {block.input['prompt'][:80]}")
            output = run_subagent(block.input["prompt"])
        else:
            handler = TOOL_HANDLERS.get(block.name)
            output = handler(**block.input) if handler else f"Unknown tool: {block.name}"
```

`task` 工具走 `run_subagent()`，其他工具照旧走 dispatch map。主 agent 收到的 `output` 是子 agent 的摘要文本 -- 和收到 `bash` 的输出没有区别，格式完全一致。

---

## 完整流程举例

用户问："这个项目用了哪些依赖，有没有安全漏洞？"

```
主 agent 思考：这个任务需要两步，分别派子 agent

Round 1:
  主 agent → task(prompt="列出项目所有依赖及版本", description="scan deps")
  子 agent 启动:
    sub_messages = [{role: "user", content: "列出项目所有依赖及版本"}]
    → bash: cat requirements.txt
    → bash: pip list
    → 总结："项目有 12 个依赖，关键: anthropic==0.30, flask==3.0..."
  主 agent 收到摘要（子 agent 的 sub_messages 已丢弃）

Round 2:
  主 agent → task(prompt="检查这些依赖的已知漏洞: anthropic==0.30, flask==3.0...", description="vuln check")
  子 agent 启动（又是全新的 sub_messages = []）
    → bash: pip-audit
    → 总结："发现 1 个漏洞: flask 3.0 有 CVE-2024-xxxx..."
  主 agent 收到摘要

Round 3:
  主 agent 综合两个摘要，给用户最终回答
```

注意：主 agent 的 messages 里只有两段简短摘要，而不是 `cat requirements.txt` 的完整输出 + `pip list` 的完整输出 + `pip-audit` 的完整输出。**上下文干净了一个数量级。**

---

## 关键洞察

| 概念 | 解释 |
|------|------|
| 子 agent 是一次性的 | 用完即扔，`sub_messages` 被垃圾回收 |
| 共享文件系统，不共享记忆 | 子 agent 能读写文件，但看不到主 agent 的对话历史 |
| 唯一区别是 task 工具 | 子 agent = 主 agent - task 工具。其他一模一样 |
| 摘要是信息压缩 | 10 轮工具调用 → 一段文字，信息损失换来上下文清洁 |
| 安全限制 30 轮 | 防止子 agent 死循环 |

---

## 跟 mattress bot 的关系

床垫 bot 的复杂查询可以用 subagent 分解。比如用户问"红星店和居然之家店这个月谁卖得好，差在哪里"：

- 子 agent 1：查红星店月数据 → 返回摘要
- 子 agent 2：查居然之家月数据 → 返回摘要
- 主 agent 对比两个摘要，给出分析

每个子 agent 只关注自己的查询，上下文不互相污染。

---

## 变更总结

| 组件 | 之前（s03） | 之后（s04） |
|------|------------|------------|
| Agent 层级 | 单层 | 双层（主 agent + 子 agent） |
| 工具集 | 所有工具平级 | PARENT_TOOLS / CHILD_TOOLS 分层 |
| 上下文隔离 | 无（所有信息堆在一个 messages 里） | 子 agent 有独立 messages，只返回摘要 |
| Agent loop | 不变 | 新增 run_subagent()，内部循环和 s01 一样 |

**总结：子 agent 是上下文隔离的核心手段。大任务拆成小任务，每个小任务在干净的环境里完成，只带一句结论回来。**
