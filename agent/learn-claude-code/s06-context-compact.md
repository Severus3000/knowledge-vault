# s06 - Context Compact（上下文压缩）

`s01 > s02 > s03 > s04 > s05 > [ s06 ] | s07 > s08 > s09 > s10 > s11 > s12`

> **核心格言**：*"上下文总会满，要有办法腾地方"* -- 旧信息主动清理，但存磁盘，不是真丢了。

---

## 问题

messages 列表只增不减。每次调用工具，tool_result 就往列表里追加内容。读 30 个文件 + 跑 20 条命令，轻松超过 100k token。

上下文窗口是有限的（128k、200k 取决于模型）。更关键的是，窗口没满之前注意力就已经稀释了 -- 第 100 条消息里的工具输出还在占位置，但 AI 的注意力早就不在那里了。token 花了钱，但没产生价值。

不压缩的话，agent 要么撞墙（context window overflow），要么在到达上限之前就开始犯糊涂。

---

## 解决方案：三层压缩策略

激进程度递增，像三道防线：

```
每轮自动          token 超阈值          AI 主动调用
    |                  |                    |
    v                  v                    v
[Layer 1]          [Layer 2]           [Layer 3]
micro_compact      auto_compact         compact 工具
  静默替换旧结果      保存+摘要替换全部      同 Layer 2
  无感，每轮执行      触发条件: >50000       AI 自己判断
```

类比：
- Layer 1 = **扔旧草稿纸** -- 自动的，你没感觉
- Layer 2 = **浓缩成一页摘要** -- 被动触发，到上限了才做
- Layer 3 = **AI 自己觉得乱了，主动整理** -- 主动触发

---

## Layer 1：micro_compact（每轮自动，静默执行）

**做什么**：把超过 3 轮的 tool_result 内容替换成占位符 `"[Previous: used {tool_name}]"`。

```python
KEEP_RECENT = 3
PRESERVE_RESULT_TOOLS = {"read_file"}

def micro_compact(messages: list) -> list:
    # 找到所有 tool_result
    tool_results = []
    for msg_idx, msg in enumerate(messages):
        if msg["role"] == "user" and isinstance(msg.get("content"), list):
            for part_idx, part in enumerate(msg["content"]):
                if isinstance(part, dict) and part.get("type") == "tool_result":
                    tool_results.append((msg_idx, part_idx, part))
    if len(tool_results) <= KEEP_RECENT:
        return messages
    # 清理旧结果，保留最近 3 条
    to_clear = tool_results[:-KEEP_RECENT]
    for _, _, result in to_clear:
        if not isinstance(result.get("content"), str) or len(result["content"]) <= 100:
            continue
        tool_id = result.get("tool_use_id", "")
        tool_name = tool_name_map.get(tool_id, "unknown")
        if tool_name in PRESERVE_RESULT_TOOLS:
            continue  # read_file 结果保留，因为是参考资料
        result["content"] = f"[Previous: used {tool_name}]"
    return messages
```

关键设计：
- **保留最近 3 条** -- `KEEP_RECENT = 3`，太旧的才压缩
- **read_file 结果不压缩** -- `PRESERVE_RESULT_TOOLS = {"read_file"}`，因为文件内容是参考资料，压缩了 AI 就得重新读文件
- **短结果不压缩** -- 100 字符以下的结果不值得压缩
- **每轮自动执行，完全无感** -- AI 不知道这件事在发生

---

## Layer 2：auto_compact（token 超阈值时触发）

**触发条件**：`estimate_tokens(messages) > 50000`

**做什么**：两步走 -- 先保存完整对话到磁盘，再用 LLM 生成摘要替换所有 messages。

```python
THRESHOLD = 50000

def auto_compact(messages: list) -> list:
    # Step 1: 完整对话保存到磁盘
    TRANSCRIPT_DIR.mkdir(exist_ok=True)
    transcript_path = TRANSCRIPT_DIR / f"transcript_{int(time.time())}.jsonl"
    with open(transcript_path, "w") as f:
        for msg in messages:
            f.write(json.dumps(msg, default=str) + "\n")

    # Step 2: 让 LLM 生成摘要
    conversation_text = json.dumps(messages, default=str)[-80000:]
    response = client.messages.create(
        model=MODEL,
        messages=[{"role": "user", "content":
            "Summarize this conversation for continuity. Include: "
            "1) What was accomplished, 2) Current state, 3) Key decisions made. "
            "Be concise but preserve critical details.\n\n" + conversation_text}],
        max_tokens=2000,
    )
    summary = response.content[0].text

    # Step 3: 摘要替换所有 messages
    return [
        {"role": "user", "content": f"[Conversation compressed. Transcript: {transcript_path}]\n\n{summary}"},
    ]
```

关键设计：
- **完整历史保存在 `.transcripts/` 目录** -- 不是真的丢了，磁盘上有备份
- **摘要包含三个维度**：完成了什么、当前状态、关键决策 -- 确保 AI 能接着干
- **messages 列表被替换成只有一条消息** -- 从几万 token 压缩到约 2000 token
- 摘要消息里包含 transcript 文件路径 -- 理论上 AI 可以用 `read_file` 重新加载历史

---

## Layer 3：compact 工具（AI 主动调用）

```python
TOOLS = [
    ...
    {"name": "compact",
     "description": "Trigger manual conversation compression.",
     "input_schema": {"type": "object", "properties": {
         "focus": {"type": "string", "description": "What to preserve in the summary"}
     }}},
]
```

机制和 Layer 2 完全一样（内部调用同一个 `auto_compact()`），区别在于触发方式：**AI 自己觉得上下文太乱了，主动调用 compact 工具**。

```python
if manual_compact:
    print("[manual compact]")
    messages[:] = auto_compact(messages)
    return
```

---

## 整合进循环

在每次调用 LLM 之前插入两行压缩逻辑，循环骨架不变：

```python
def agent_loop(messages: list):
    while True:
        # Layer 1: micro_compact before each LLM call
        micro_compact(messages)
        # Layer 2: auto_compact if token estimate exceeds threshold
        if estimate_tokens(messages) > THRESHOLD:
            print("[auto_compact triggered]")
            messages[:] = auto_compact(messages)

        response = client.messages.create(
            model=MODEL, system=SYSTEM, messages=messages,
            tools=TOOLS, max_tokens=8000,
        )
        # ... 后面和之前一模一样
```

循环结构不变，只在 LLM 调用前加了两行防御。这就是从 s01 一路过来保持循环稳定的价值 -- 新机制插入进来，不破坏已有逻辑。

---

## 关键细节：`messages[:] = auto_compact(messages)`

为什么是 `messages[:] =` 而不是 `messages = `？

因为 `messages` 是从外部传进来的列表。`messages = auto_compact(...)` 只会重新绑定局部变量，外面的列表不会变。`messages[:] = auto_compact(...)` 是**就地替换列表内容**，外面的 `history` 也会同步更新。

---

## token 估算

```python
def estimate_tokens(messages: list) -> int:
    return len(str(messages)) // 4
```

粗略估算：约 4 个字符 = 1 个 token。不精确但够用 -- 压缩阈值不需要精确到个位数，差 20% 无所谓。

---

## 完整流程举例

```
Turn 1-10:  正常对话，micro_compact 静默清理旧 tool_result
            tokens: 8000 → 15000 → 25000 → 40000

Turn 11:    tokens 估算 = 52000，超过阈值
            [auto_compact triggered]
            完整对话保存到 .transcripts/transcript_1712345678.jsonl
            LLM 生成摘要 → messages 被压缩到 ~2000 token
            AI 继续工作，看到的是摘要 + 新的 tool_result

Turn 12-20: 又积累了一堆上下文
            micro_compact 继续静默工作

Turn 18:    AI 自己觉得上下文混乱 → 调用 compact 工具
            [manual compact]
            再次压缩 → 干净的重新开始
```

---

## s01-s06 能力总结

到 s06 为止，我们的 agent harness 已经具备了完整的基础能力：

| Session | 能力 | 一句话 |
|---------|------|--------|
| **s01** | 行动 | 一个循环 + bash = agent |
| **s02** | 多工具 | dispatch map，加工具不改循环 |
| **s03** | 规划 | TodoManager，先列步骤再动手 |
| **s04** | 分工 | Subagent，大任务拆小，上下文隔离 |
| **s05** | 学知识 | Skill loading，按需加载领域知识 |
| **s06** | 管记忆 | Context compact，三层压缩保持头脑清醒 |

从 s07 开始是更高级的能力（任务系统、多 agent 协作、worktree 隔离等），主要面向复杂的编码 agent 场景。对于我们的床垫 bot，**s01-s06 是核心路径**。

---

## 核心设计原则

**上下文是稀缺资源。** 不是"有多少用多少"，而是要主动管理：

- 旧信息不再有用 → 替换成占位符（micro_compact）
- 上下文快满了 → 压缩成摘要，原文存磁盘（auto_compact）
- AI 自己判断需要整理 → 给它一个工具让它自己触发（compact）

完整历史永远在磁盘上，不是真的丢了。压缩的本质是**用信息损失换来注意力集中** -- 和 s04 子 agent 的思路一脉相承。

---

## 变更总结

| 组件 | 之前（s05） | 之后（s06） |
|------|------------|------------|
| 上下文管理 | 无（messages 无限增长） | 三层压缩策略 |
| 新增工具 | 无 | `compact`（AI 主动触发压缩） |
| 新增函数 | 无 | `micro_compact()`, `auto_compact()`, `estimate_tokens()` |
| 磁盘存储 | 无 | `.transcripts/` 目录保存完整对话 |
| Agent loop | 循环前加两行压缩检查 | 骨架不变 |

**总结：上下文总会满，但满了不可怕 -- 旧信息压缩成摘要，原文存磁盘，AI 在干净的上下文里继续工作。**
