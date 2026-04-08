# s11 - Autonomous Agents（自治 Agent）

`s01 > s02 > s03 > s04 > s05 > s06 | s07 > s08 > s09 > s10 > [ s11 ] s12`

> **核心格言**：*"队友自己看看板，有活就认领"* -- 自组织，看板驱动。

---

## 问题

s09-s10 的队友虽然能通信、能协议，但**本质上还是被动的** -- 领导 spawn 时给一个 prompt，做完就闲在那里等领导发新消息。如果领导忘了分配任务，队友就一直 IDLE。

这不 scale：
- 领导需要记住每个队友的状态、手动分配任务
- 领导自己也是 AI，上下文压缩后可能忘了谁在做什么
- N 个队友意味着 N 倍的管理负担

需要的是：**队友自己去看板上找活干，不需要领导逐个分配。** 从"推"（领导推任务给队友）变成"拉"（队友自己拉任务）。

---

## 解决方案：WORK/IDLE 双阶段循环

```
spawn("alice", "coder", "初始任务")
  |
  v
+===========+
‖   WORK    ‖ ← 标准 agent loop（跟 s01 一样）
‖           ‖   每轮检查收件箱
‖           ‖   调用工具干活
+===========+
  |
  | stop_reason != "tool_use"（LLM 觉得做完了）
  | 或者 AI 主动调用 idle 工具
  v
+===========+
‖   IDLE    ‖ ← 每 5 秒轮询一次，最多 60 秒
‖           ‖
‖  +--------v---------+
‖  | 查收件箱          | → 有消息？→ 回到 WORK
‖  +-------------------+
‖  | 扫描任务看板       | → 有 unclaimed？→ 认领 → 回到 WORK
‖  +-------------------+
‖  | 超时 60 秒         | → 自动关机
‖  +-------------------+
+===========+
```

两个阶段无限循环，直到 60 秒没活干自动关机。

---

## IDLE 阶段详解

```python
# -- IDLE PHASE --
self._set_status(name, "idle")
resume = False
polls = IDLE_TIMEOUT // max(POLL_INTERVAL, 1)  # 60 / 5 = 12 次

for _ in range(polls):
    time.sleep(POLL_INTERVAL)  # 5 seconds

    # Check 1: inbox messages
    inbox = BUS.read_inbox(name)
    if inbox:
        for msg in inbox:
            if msg.get("type") == "shutdown_request":
                self._set_status(name, "shutdown")
                return
            messages.append({"role": "user", "content": json.dumps(msg)})
        resume = True
        break

    # Check 2: unclaimed tasks on the board
    unclaimed = scan_unclaimed_tasks()
    if unclaimed:
        task = unclaimed[0]
        result = claim_task(task["id"], name)
        if result.startswith("Error:"):
            continue  # someone else claimed it first
        task_prompt = (
            f"<auto-claimed>Task #{task['id']}: {task['subject']}\n"
            f"{task.get('description', '')}</auto-claimed>"
        )
        messages.append({"role": "user", "content": task_prompt})
        resume = True
        break

if not resume:
    self._set_status(name, "shutdown")
    return  # 60s no work → auto-shutdown
```

每 5 秒做两件事：

1. **查收件箱** -- 有消息就注入 messages，回到 WORK 阶段
2. **扫描任务看板** -- 找 unclaimed 任务，认领后回到 WORK 阶段

如果 60 秒（12 次轮询）都没找到活干，自动关机。不浪费线程资源。

---

## scan_unclaimed_tasks -- 看板扫描

```python
def scan_unclaimed_tasks() -> list:
    TASKS_DIR.mkdir(exist_ok=True)
    unclaimed = []
    for f in sorted(TASKS_DIR.glob("task_*.json")):
        task = json.loads(f.read_text())
        if (task.get("status") == "pending"
                and not task.get("owner")
                and not task.get("blockedBy")):
            unclaimed.append(task)
    return unclaimed
```

三个条件同时满足才算 unclaimed：
- `status == "pending"` -- 还没开始
- `owner` 为空 -- 没人认领
- `blockedBy` 为空 -- 没有被卡住

这就是 s07 任务图的价值 -- 依赖关系自动过滤掉还不能做的任务。

## claim_task -- 认领（带竞争保护）

```python
def claim_task(task_id: int, owner: str) -> str:
    with _claim_lock:
        task = json.loads(path.read_text())
        if task.get("owner"):
            return f"Error: Task {task_id} has already been claimed by {task['owner']}"
        if task.get("status") != "pending":
            return f"Error: Task {task_id} cannot be claimed because its status is '{task['status']}'"
        task["owner"] = owner
        task["status"] = "in_progress"
        path.write_text(json.dumps(task, indent=2))
    return f"Claimed task #{task_id} for {owner}"
```

`_claim_lock` 是 `threading.Lock()`。如果 alice 和 bob 同时看到 task 3 是 unclaimed，只有一个能成功认领，另一个会收到 `"Error: already claimed"`。

---

## 身份重注入

s06 压缩后，messages 可能只剩 1-3 条（摘要 + 最近几条）。队友的身份信息（名字、角色、团队）在原始 system prompt 里还在，但 messages 上下文里的身份线索可能丢失了。

```python
def make_identity_block(name: str, role: str, team_name: str) -> dict:
    return {
        "role": "user",
        "content": f"<identity>You are '{name}', role: {role}, team: {team_name}. Continue your work.</identity>",
    }
```

在自动认领新任务时，如果 messages 很短（压缩过），在开头插入身份块：

```python
if len(messages) <= 3:
    messages.insert(0, make_identity_block(name, role, team_name))
    messages.insert(1, {"role": "assistant", "content": f"I am {name}. Continuing."})
messages.append({"role": "user", "content": task_prompt})
```

这样即使上下文被压缩过，AI 仍然知道"我是 alice，我是 coder，我属于 default 团队"。

---

## 完整流程举例

```
Round 1: 领导创建一批任务到看板
  > task_create: {subject: "实现用户注册 API"}       → task 1
  > task_create: {subject: "实现用户登录 API"}       → task 2
  > task_create: {subject: "写注册页面"}             → task 3, blockedBy: [1]
  > task_create: {subject: "写登录页面"}             → task 4, blockedBy: [2]
  > spawn_teammate: {name: "alice", role: "backend", prompt: "你是后端开发"}
  > spawn_teammate: {name: "bob", role: "frontend", prompt: "你是前端开发"}

  此时看板：
  [ ] #1: 实现用户注册 API           ← unclaimed, 可认领
  [ ] #2: 实现用户登录 API           ← unclaimed, 可认领
  [ ] #3: 写注册页面 (blocked by: [1]) ← blocked, 不可认领
  [ ] #4: 写登录页面 (blocked by: [2]) ← blocked, 不可认领

Alice 线程:
  WORK: 完成初始 prompt
  IDLE: scan_unclaimed_tasks() → 看到 task 1 和 task 2
        claim_task(1, "alice") → 成功
  WORK: 实现用户注册 API
        task_update(1, status="completed")
        → _clear_dependency(1) → task 3 的 blockedBy 变空
  IDLE: scan_unclaimed_tasks() → 看到 task 3（刚解锁）
        claim_task(3, "alice") → 成功
  WORK: 写注册页面...

Bob 线程（并行）:
  WORK: 完成初始 prompt
  IDLE: scan_unclaimed_tasks() → 看到 task 1 和 task 2
        claim_task(1, "bob") → Error: already claimed by alice
        claim_task(2, "bob") → 成功
  WORK: 实现用户登录 API
        task_update(2, status="completed")
        → _clear_dependency(2) → task 4 的 blockedBy 变空
  IDLE: scan_unclaimed_tasks() → 看到 task 4
        claim_task(4, "bob") → 成功
  WORK: 写登录页面...
```

领导只做了一件事：创建任务 + spawn 队友。**任务分配完全自动化** -- alice 和 bob 自己看看板、自己认领、自己处理依赖顺序。

---

## 从"推"到"拉"

| 模式 | s09-s10（推） | s11（拉） |
|------|-------------|----------|
| 任务分配 | 领导 send_message 给具体队友 | 队友自己扫描看板 |
| 领导负担 | 记住每个人的状态，手动分配 | 只管创建任务和 spawn |
| 扩展性 | N 个队友 = N 倍管理 | 队友自组织 |
| 空闲处理 | 等领导发消息 | 自动关机，不浪费资源 |

---

## 变更总结

| 组件 | 之前（s10） | 之后（s11） |
|------|------------|------------|
| 队友行为 | 被动等指令 | 主动扫描看板认领任务 |
| 循环结构 | 单阶段（WORK） | 双阶段（WORK → IDLE → WORK → ...） |
| 新增函数 | 无 | `scan_unclaimed_tasks()`, `claim_task()`, `make_identity_block()` |
| 新增工具 | 无 | `idle`（队友主动进入 IDLE）, `claim_task`（认领任务） |
| 竞争保护 | 无 | `_claim_lock` 防止多人认领同一任务 |
| 自动关机 | 无 | 60 秒没活干自动 shutdown |
| 身份管理 | 仅 system prompt | 压缩后重注入 identity block |

**总结：从领导推任务变成队友自己拉任务。看板驱动 + 自动认领 + 超时关机 = 自组织团队。领导只需要创建任务和 spawn 队友，剩下的让他们自己搞定。**
