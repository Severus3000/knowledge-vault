# s08 - Background Tasks（后台任务）

`s01 > s02 > s03 > s04 > s05 > s06 | s07 > [ s08 ] s09 > s10 > s11 > s12`

> **核心格言**：*"慢操作丢后台，agent 继续想下一步"* -- AI 思考是单线程的，I/O 可以并行。

---

## 问题

s01 到 s07 的循环都是**阻塞式**的。AI 调用 `bash("npm install")`，harness 执行 `subprocess.run()`，整个循环卡住等 npm 装完（可能 30 秒）。这段时间 AI 什么都不能干 -- 不能思考下一步、不能同时跑测试、不能并行做别的事。

如果 AI 需要跑 `npm install` + `pytest` + `cargo build` 三个慢命令，串行执行要 90 秒。但这三个命令之间没有依赖关系，完全可以同时跑。

类比：**厨师炖汤**。把汤放进锅里后，厨师不需要站在锅前盯着等 30 分钟 -- 他可以去切菜、洗碗、备料。汤好了，厨房计时器响一声就行。

---

## 解决方案：守护线程 + 通知队列

```
Main thread (agent loop)              Background threads
+--------------------------+          +-----------------+
| LLM call                 |          | npm install     |
| ...                      |          | (30s)           |
| background_run("npm i")  | -------> |                 |
| result: "task abc started"|         |                 |
|                          |          |  done → enqueue |
| LLM call (continues)    |          +-----------------+
| ...                      |
| background_run("pytest") | -------> +-----------------+
| result: "task def started"|         | pytest          |
|                          |          | (20s)           |
| [drain_notifications]    |          |  done → enqueue |
| "npm install completed"  | <-----  +-----------------+
| → inject into messages   |
+--------------------------+
```

两个核心组件：
1. **守护线程** -- 每个后台命令在独立线程里跑，`daemon=True` 确保主进程退出时线程也退出
2. **通知队列** -- 命令完成后，结果放进队列；主循环每轮开始前检查队列（drain）

---

## BackgroundManager 类

```python
class BackgroundManager:
    def __init__(self):
        self.tasks = {}            # task_id -> {status, result, command}
        self._notification_queue = []  # completed results waiting to be drained
        self._lock = threading.Lock()  # thread-safe access to queue
```

三个数据结构：
- `tasks` -- 所有后台任务的注册表
- `_notification_queue` -- 完成通知的缓冲区
- `_lock` -- 线程锁，防止主线程和后台线程同时写队列

### run() -- 启动后台任务

```python
def run(self, command: str) -> str:
    task_id = str(uuid.uuid4())[:8]
    self.tasks[task_id] = {"status": "running", "result": None, "command": command}
    thread = threading.Thread(
        target=self._execute, args=(task_id, command), daemon=True
    )
    thread.start()
    return f"Background task {task_id} started: {command[:80]}"
```

关键：`thread.start()` 之后**立刻 return**。AI 收到的 tool_result 是 `"Background task abc started"`，而不是命令执行结果。命令还在后台跑着。

### _execute() -- 后台线程的执行逻辑

```python
def _execute(self, task_id: str, command: str):
    try:
        r = subprocess.run(
            command, shell=True, cwd=WORKDIR,
            capture_output=True, text=True, timeout=300  # 5min timeout
        )
        output = (r.stdout + r.stderr).strip()[:50000]
        status = "completed"
    except subprocess.TimeoutExpired:
        output = "Error: Timeout (300s)"
        status = "timeout"
    # Push result to notification queue
    self.tasks[task_id]["status"] = status
    self.tasks[task_id]["result"] = output or "(no output)"
    with self._lock:
        self._notification_queue.append({
            "task_id": task_id,
            "status": status,
            "command": command[:80],
            "result": (output or "(no output)")[:500],
        })
```

这个方法跑在**后台线程**里。完成后不直接通知 AI，而是把结果放进 `_notification_queue`。`with self._lock` 确保线程安全。

### drain_notifications() -- 取出所有完成通知

```python
def drain_notifications(self) -> list:
    with self._lock:
        notifs = list(self._notification_queue)
        self._notification_queue.clear()
    return notifs
```

取出所有待处理通知，清空队列。**drain-on-read** 模式 -- 读一次就清空，不会重复处理。

---

## 循环变化：每轮开始前 drain

```python
def agent_loop(messages: list):
    while True:
        # Drain background notifications before LLM call
        notifs = BG.drain_notifications()
        if notifs and messages:
            notif_text = "\n".join(
                f"[bg:{n['task_id']}] {n['status']}: {n['result']}" for n in notifs
            )
            messages.append({
                "role": "user",
                "content": f"<background-results>\n{notif_text}\n</background-results>"
            })

        response = client.messages.create(
            model=MODEL, system=SYSTEM, messages=messages,
            tools=TOOLS, max_tokens=8000,
        )
        # ... rest unchanged
```

在每次 LLM 调用之前，检查有没有后台任务完成了。如果有，把结果包装成 `<background-results>` 消息注入 `messages`。AI 在下一轮就能看到后台任务的结果。

---

## 时间线图

```
时间 →
AI:     [spawn A]---[spawn B]---[思考其他事]---[看到 A 结果]---[看到 B 结果]
         |            |
Thread:  |-- A 执行 (30s) --→ enqueue
                      |-- B 执行 (20s) --→ enqueue

传统串行: [等 A 30s]---------[等 B 20s]--------- = 50s 什么都不干
后台并行: [spawn A][spawn B][干别的事]             = AI 不阻塞
```

---

## Dispatch Map 加两行

```python
TOOL_HANDLERS = {
    "bash":             lambda **kw: run_bash(kw["command"]),           # blocking
    "read_file":        lambda **kw: run_read(kw["path"], kw.get("limit")),
    "write_file":       lambda **kw: run_write(kw["path"], kw["content"]),
    "edit_file":        lambda **kw: run_edit(kw["path"], kw["old_text"], kw["new_text"]),
    "background_run":   lambda **kw: BG.run(kw["command"]),             # non-blocking
    "check_background": lambda **kw: BG.check(kw.get("task_id")),      # query status
}
```

注意：`bash` 还在，是阻塞的。`background_run` 是非阻塞的。AI 自己决定哪些命令值得后台跑（慢的），哪些直接跑（快的）。

---

## 完整流程举例

用户说："跑一下测试和 lint，然后告诉我结果"

```
Round 1:
  AI 思考：两个命令互不依赖，可以并行
  > background_run: {"command": "pytest tests/ -v"}
    → "Background task abc12345 started"
  > background_run: {"command": "flake8 src/"}
    → "Background task def67890 started"

Round 2:
  [drain_notifications] → flake8 先跑完（快）
  messages 里注入：
    <background-results>
    [bg:def67890] completed: src/main.py:42: E501 line too long
    </background-results>

  AI 看到 flake8 结果，先处理 lint 问题
  > edit_file: 修复 line too long

Round 3:
  [drain_notifications] → pytest 也跑完了
  messages 里注入：
    <background-results>
    [bg:abc12345] completed: 15 passed, 2 failed
    </background-results>

  AI 看到测试结果，报告给用户
```

AI 没有干等 -- flake8 和 pytest 同时跑，结果陆续回来，AI 可以在等待期间做别的事。

---

## 变更总结

| 组件 | 之前（s07） | 之后（s08） |
|------|------------|------------|
| 执行模式 | 全部阻塞 | 阻塞（bash）+ 非阻塞（background_run） |
| 新增类 | 无 | BackgroundManager |
| 新增工具 | 无 | `background_run`, `check_background` |
| 循环变化 | 无 | 每轮开始前 drain_notifications |
| 线程模型 | 单线程 | 主线程 + N 个守护线程 |

**总结：慢操作不需要等。丢进后台线程，结果通过通知队列回来。AI 的思考是单线程的，但 I/O 可以并行 -- 这是"等着"和"高效利用时间"的区别。**

---

## Python 并发知识点

本节涉及的 Python 并发知识已整理到独立笔记，详见：

- [[concurrency-overview]] — 三种并发方式总览（线程/进程/异步）及 agent 场景对应
- [[threading]] — 线程详解：start、join、daemon
- [[thread-safety]] — 竞态条件、锁/互斥锁、drain 排空模式
- [[process]] — 进程、IPC、Claude Code parallel agent
- [[async-await]] — 异步、await、event loop

笔记路径：`python/concurrency/`
