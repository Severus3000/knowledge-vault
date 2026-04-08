# s03 - TodoWrite（待办写入）

`s01 > s02 > [ s03 ] s04 > s05 > s06 | s07 > s08 > s09 > s10 > s11 > s12`

> **核心格言**：*"没有计划的 agent 走哪算哪"* -- 先列步骤再动手，完成率翻倍。

---

## 问题

多步任务中，AI 会迷路。

一个 10 步重构任务，AI 做完第 1-3 步之后开始即兴发挥 -- 重复做过的事、跳过步骤、跑偏到不相关的事情上。原因很直接：**对话越长，注意力越被稀释**。工具结果不断填满上下文窗口，system prompt 的影响力逐渐被挤到边缘，第 4-10 步的计划早就被推出 AI 的注意力范围了。

这不是 AI "笨"，而是 transformer 注意力机制的结构性限制。

---

## 解决方案：TodoManager + Nag Reminder

两个机制配合：

1. **TodoManager** -- 给 AI 一个工具来记录和追踪自己的计划
2. **Nag Reminder** -- 如果 AI 连续几轮不更新计划，自动催促

```
+--------+      +-------+      +---------+
|  User  | ---> |  LLM  | ---> | Tools   |
| prompt |      |       |      | + todo  |
+--------+      +---+---+      +----+----+
                    ^                |
                    |   tool_result  |
                    +----------------+
                          |
              +-----------+-----------+
              | TodoManager state     |
              | [ ] task A            |
              | [>] task B  <- doing  |
              | [x] task C            |
              +-----------------------+
                          |
              if rounds_since_todo >= 3:
                inject <reminder>
```

设计思想：**不能替 AI 画路线**（那就变成硬编码流程了），但可以给它一个**自己记录路线的工具**，再**时不时催一下**。

---

## TodoManager 详解

### 数据结构

```python
class TodoManager:
    def __init__(self):
        self.items = []  # list of {id, text, status}
```

`items` 是一个列表，每个 item 有三个字段：`id`、`text`（描述）、`status`（状态）。

### update() 方法 -- 全量覆盖

```python
def update(self, items: list) -> str:
    if len(items) > 20:
        raise ValueError("Max 20 todos allowed")
    validated = []
    in_progress_count = 0
    for i, item in enumerate(items):
        text = str(item.get("text", "")).strip()
        status = str(item.get("status", "pending")).lower()
        item_id = str(item.get("id", str(i + 1)))
        if not text:
            raise ValueError(f"Item {item_id}: text required")
        if status not in ("pending", "in_progress", "completed"):
            raise ValueError(f"Item {item_id}: invalid status '{status}'")
        if status == "in_progress":
            in_progress_count += 1
        validated.append({"id": item_id, "text": text, "status": status})
    if in_progress_count > 1:
        raise ValueError("Only one task can be in_progress at a time")
    self.items = validated
    return self.render()
```

关键设计：

| 规则 | 原因 |
|------|------|
| **全量覆盖**，不是增量更新 | AI 每次传完整列表，不用追踪"改了哪条"。简单粗暴但可靠 |
| **最多 20 个** | 防止 AI 列出 100 个微步骤，撑爆上下文 |
| **只允许 3 种状态** | `pending`（待做）、`in_progress`（进行中）、`completed`（完成）-- 不多不少 |
| **`in_progress` 最多 1 个** | 这是最关键的约束 -- **强制 AI 一次只做一件事**。如果允许多个同时进行，AI 会并行乱窜 |
| **验证会抛异常** | 而不是默默忽略错误。AI 能看到异常消息并修正 |

### render() 方法 -- 给 AI 一面镜子

```python
def render(self) -> str:
    if not self.items:
        return "No todos."
    lines = []
    for item in self.items:
        marker = {
            "pending": "[ ]",
            "in_progress": "[>]",
            "completed": "[x]"
        }[item["status"]]
        lines.append(f"{marker} #{item['id']}: {item['text']}")
    done = sum(1 for t in self.items if t["status"] == "completed")
    lines.append(f"\n({done}/{len(self.items)} completed)")
    return "\n".join(lines)
```

渲染输出示例：

```
[ ] #1: Add type hints to all functions
[>] #2: Write docstrings
[ ] #3: Add main guard
[x] #4: Fix import order

(1/4 completed)
```

这个输出作为 `tool_result` 喂回给 AI。效果是：每次 AI 更新 todo，它都能**看到自己的进度**。这比 system prompt 里写"记得跟踪进度"有效一百倍 -- 因为 `tool_result` 在消息列表的末尾，是 AI 最新看到的内容，注意力权重最高。

---

## Dispatch Map 只多加一行

```python
TOOL_HANDLERS = {
    "bash":       lambda **kw: run_bash(kw["command"]),
    "read_file":  lambda **kw: run_read(kw["path"], kw.get("limit")),
    "write_file": lambda **kw: run_write(kw["path"], kw["content"]),
    "edit_file":  lambda **kw: run_edit(kw["path"], kw["old_text"], kw["new_text"]),
    "todo":       lambda **kw: TODO.update(kw["items"]),  # <-- only new line
}
```

跟 s02 比，字典就多了一行。dispatch map 模式的价值在这里体现得淋漓尽致。

---

## 循环的变化

s03 的循环相比 s02 只加了两个东西：

### 1. rounds_since_todo 计数器

```python
def agent_loop(messages: list):
    rounds_since_todo = 0  # <-- new
    while True:
        response = client.messages.create(
            model=MODEL, system=SYSTEM, messages=messages,
            tools=TOOLS, max_tokens=8000,
        )
        messages.append({"role": "assistant", "content": response.content})
        if response.stop_reason != "tool_use":
            return
```

### 2. Nag reminder 注入 + try/except 包装

```python
        results = []
        used_todo = False
        for block in response.content:
            if block.type == "tool_use":
                handler = TOOL_HANDLERS.get(block.name)
                try:  # <-- new: try/except wraps tool calls
                    output = handler(**block.input) if handler \
                        else f"Unknown tool: {block.name}"
                except Exception as e:
                    output = f"Error: {e}"
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(output),
                })
                if block.name == "todo":
                    used_todo = True

        # Reset or increment counter
        rounds_since_todo = 0 if used_todo else rounds_since_todo + 1

        # Nag reminder injection  <-- new
        if rounds_since_todo >= 3:
            results.append({
                "type": "text",
                "text": "<reminder>Update your todos.</reminder>"
            })

        messages.append({"role": "user", "content": results})
```

两个新机制：

| 机制 | 作用 |
|------|------|
| **`try/except`** | TodoManager 的验证会抛异常（比如 `in_progress` 超过 1 个）。包一层 try/except 让异常变成错误消息喂回给 AI，而不是崩掉整个循环 |
| **Nag reminder** | 连续 3 轮没用 todo 工具 → 在 tool_results 后面追加一条 `<reminder>` 文本。AI 下一轮就能看到催促，通常会立即更新 todo |

注意 nag reminder 是追加在 `results` 列表中（跟 tool_results 一起作为 user 消息发送），不是修改 system prompt。这保证催促出现在消息列表的末尾，注意力权重最高。

---

## 完整流程举例

用户要求："创建一个 Python 包，包含 `__init__.py`、`utils.py` 和 `tests/test_utils.py`"

```
Round 1: AI 调用 todo 工具
  items = [
    {id: "1", text: "Create package directory",      status: "in_progress"},
    {id: "2", text: "Create __init__.py",             status: "pending"},
    {id: "3", text: "Create utils.py with functions",  status: "pending"},
    {id: "4", text: "Create tests/test_utils.py",      status: "pending"},
  ]
  → TodoManager 验证通过，返回渲染结果
  → rounds_since_todo = 0

Round 2: AI 调用 bash 创建目录
  $ mkdir -p mypackage/tests
  → rounds_since_todo = 1

Round 3: AI 调用 todo 更新 + write_file
  #1 completed, #2 in_progress
  写入 __init__.py
  → rounds_since_todo = 0

Round 4-5: AI 继续写文件
  → rounds_since_todo = 1, 2

Round 6: AI 还是没更新 todo
  → rounds_since_todo = 3
  → 注入 <reminder>Update your todos.</reminder>

Round 7: AI 看到 reminder，更新 todo
  #2 #3 completed, #4 in_progress
  → rounds_since_todo = 0

Round 8: AI 写测试文件，更新 todo 全部 completed
  → stop_reason = "end_turn", 循环结束
```

---

## System Prompt 也更新了

```python
SYSTEM = f"""You are a coding agent at {WORKDIR}.
Use the todo tool to plan multi-step tasks. Mark in_progress before starting, completed when done.
Prefer tools over prose."""
```

跟 s01/s02 比，多了对 todo 工具的使用指导。但注意：这只是**建议**，不是硬性控制。AI 可以忽略这个建议 -- 所以才需要 nag reminder 作为"软强制"。

---

## 设计哲学

这个 session 最深刻的洞察：

> **不能替 AI 画路线（那就变成硬编码流程），给它一个自己记录路线的工具，再时不时催一下。**

| 方案 | 问题 |
|------|------|
| 硬编码步骤（step 1 → step 2 → ...） | 失去灵活性，AI 不能根据实际情况调整计划 |
| 完全放任 | AI 会迷路，尤其在长对话中 |
| **TodoManager + Nag** | 折中：AI 自主规划，系统提供结构化工具 + 定期催促 |

类比：TodoManager 是给 AI 的**记事本**，nag reminder 是**闹钟**。你不会替员工写工作计划，但你会给他一个本子和一个每小时响一次的提醒。

---

## s01 → s02 → s03 演进总结

| Session | 加了什么 | 循环改了什么 | 核心概念 |
|---------|---------|-------------|---------|
| **s01** | bash 工具 | 创建循环本身 | ReAct 循环：while True + stop_reason |
| **s02** | read/write/edit 工具 | 硬编码 → 字典查找（1 行） | Dispatch map：循环和工具解耦 |
| **s03** | todo 工具 | +计数器 +nag reminder +try/except | 自主规划：AI 管理自己的进度 |

三个 session 下来，agent harness 的骨架已经成型：
- **循环**负责驱动（s01）
- **工具**负责执行（s02）
- **规划**负责导航（s03）

后续 session 继续在这个骨架上叠加：s04 加子 agent 分解复杂任务，s05 加按需加载的领域知识，s06 加上下文压缩防止对话过长。但**核心循环始终是 s01 那个 while True**。
