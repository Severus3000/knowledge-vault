# s12 - Worktree + Task Isolation（Worktree 任务隔离）

`s01 > s02 > s03 > s04 > s05 > s06 | s07 > s08 > s09 > s10 > s11 > [ s12 ]`

> **核心格言**：*"各干各的目录，互不干扰"* -- 任务管目标，worktree 管目录，按 ID 绑定。

---

## 问题

s11 的多 agent 团队共享同一个工作目录。alice 在改 `auth.py`，bob 也在改 `auth.py` -- 两个线程同时写同一个文件，结果不可预测。

类比：两个厨师共用一个案板。一个在切菜，另一个把切好的菜推到一边开始揉面。案板上一片混乱。

更好的做法：每个厨师有自己的案板，互不干扰。完成后把成品放到公共区域。

---

## 解决方案：每个任务绑定一个 git worktree

git worktree 是 git 的内置功能 -- 在同一个仓库里创建多个工作目录，每个目录对应一个分支。文件互不干扰，但共享同一个 git 历史。

```
项目根目录/
  .tasks/                          ← Control plane（做什么）
    task_12.json
      {"id": 12, "subject": "重构认证", "worktree": "auth-refactor"}

  .worktrees/                      ← Execution plane（在哪做）
    index.json                     ← 所有 worktree 的注册表
    events.jsonl                   ← 生命周期事件日志
    auth-refactor/                 ← 独立工作目录
      auth.py                      ← alice 的版本
      ...
    fix-login-bug/                 ← 另一个独立工作目录
      auth.py                      ← bob 的版本（和 alice 的互不影响）
      ...
```

---

## 两个平面

| 平面 | 目录 | 管什么 | 核心类 |
|------|------|--------|--------|
| **Control plane** | `.tasks/` | 做什么（目标、状态、依赖） | TaskManager |
| **Execution plane** | `.worktrees/` | 在哪做（目录、分支） | WorktreeManager |

两个平面通过 `task_id` 绑定：

```json
// .tasks/task_12.json
{"id": 12, "subject": "重构认证", "worktree": "auth-refactor", "status": "in_progress"}

// .worktrees/index.json
{"worktrees": [
  {"name": "auth-refactor", "path": ".../.worktrees/auth-refactor",
   "branch": "wt/auth-refactor", "task_id": 12, "status": "active"}
]}
```

---

## WorktreeManager 类

### create() -- 创建 worktree 并绑定任务

```python
def create(self, name: str, task_id: int = None, base_ref: str = "HEAD") -> str:
    self._validate_name(name)
    path = self.dir / name
    branch = f"wt/{name}"

    # Step 1: git worktree add
    self._run_git(["worktree", "add", "-b", branch, str(path), base_ref])

    # Step 2: register in index.json
    entry = {
        "name": name, "path": str(path), "branch": branch,
        "task_id": task_id, "status": "active", "created_at": time.time(),
    }
    idx = self._load_index()
    idx["worktrees"].append(entry)
    self._save_index(idx)

    # Step 3: bind task → worktree
    if task_id is not None:
        self.tasks.bind_worktree(task_id, name)

    return json.dumps(entry, indent=2)
```

一次创建做三件事：
1. `git worktree add` 创建独立工作目录和分支
2. 在 `index.json` 注册
3. 在 task JSON 里记录 worktree 名称

### run() -- 在 worktree 目录里执行命令

```python
def run(self, name: str, command: str) -> str:
    wt = self._find(name)
    path = Path(wt["path"])
    r = subprocess.run(
        command, shell=True,
        cwd=path,               # key: cwd is the worktree directory
        capture_output=True, text=True, timeout=300,
    )
    return (r.stdout + r.stderr).strip()[:50000]
```

关键在 `cwd=path` -- 命令在 worktree 的目录里执行，而不是项目根目录。这意味着 `ls`、`cat`、`python` 等命令看到的都是这个 worktree 的文件。

### remove() -- 删除 worktree

```python
def remove(self, name: str, force: bool = False, complete_task: bool = False) -> str:
    wt = self._find(name)

    # git worktree remove
    args = ["worktree", "remove"]
    if force:
        args.append("--force")
    args.append(wt["path"])
    self._run_git(args)

    # Optionally complete the bound task
    if complete_task and wt.get("task_id") is not None:
        self.tasks.update(wt["task_id"], status="completed")
        self.tasks.unbind_worktree(wt["task_id"])

    # Update index status
    for item in idx.get("worktrees", []):
        if item.get("name") == name:
            item["status"] = "removed"
```

### keep() -- 保留 worktree

```python
def keep(self, name: str) -> str:
    # Mark as "kept" -- directory stays, lifecycle tracked
    item["status"] = "kept"
```

收尾有两种选择：
- **remove** -- 删除目录，分支可以合并回主分支
- **keep** -- 保留目录，以后继续用

---

## 事件流（EventBus）

```python
class EventBus:
    def __init__(self, event_log_path: Path):
        self.path = event_log_path  # .worktrees/events.jsonl

    def emit(self, event: str, task: dict = None, worktree: dict = None, error: str = None):
        payload = {"event": event, "ts": time.time(), "task": task, "worktree": worktree}
        with self.path.open("a") as f:
            f.write(json.dumps(payload) + "\n")
```

append-only 的事件日志，记录所有生命周期事件：

```jsonl
{"event": "worktree.create.before", "ts": 1712345678, "task": {"id": 12}, "worktree": {"name": "auth-refactor"}}
{"event": "worktree.create.after", "ts": 1712345679, "task": {"id": 12}, "worktree": {"name": "auth-refactor", "status": "active"}}
{"event": "worktree.remove.before", "ts": 1712349999, "task": {"id": 12}, "worktree": {"name": "auth-refactor"}}
{"event": "task.completed", "ts": 1712350000, "task": {"id": 12, "status": "completed"}}
{"event": "worktree.remove.after", "ts": 1712350001, "worktree": {"name": "auth-refactor", "status": "removed"}}
```

用途：调试、审计、崩溃恢复。如果 `worktree.create.after` 存在但没有 `worktree.remove.after`，说明这个 worktree 还活着（或者创建后崩溃了）。

---

## 崩溃恢复

如果进程崩溃了怎么办？所有状态都在文件里：

- `.tasks/task_12.json` -- 任务状态
- `.worktrees/index.json` -- worktree 注册表
- `.worktrees/events.jsonl` -- 事件日志

重启后，读 index.json 就能知道有哪些 worktree、绑定了哪些任务、当前状态是什么。git worktree 目录本身也还在磁盘上。不需要内存中的任何状态。

---

## 两个状态机

```
Task FSM:                      Worktree FSM:
pending → in_progress → completed    absent → active → removed
                                                    → kept
```

| Task 状态 | 含义 |
|-----------|------|
| pending | 还没开始 |
| in_progress | 有人在做（绑定了 worktree） |
| completed | 做完了（worktree 已 remove 或 keep） |

| Worktree 状态 | 含义 |
|---------------|------|
| absent | 还没创建 |
| active | 正在使用 |
| removed | 已删除（目录清理了） |
| kept | 保留中（目录还在） |

---

## 完整流程举例

```
Round 1: 创建任务 + worktree
  > task_create: {subject: "重构认证模块"}               → task 12
  > worktree_create: {name: "auth-refactor", task_id: 12}
    → git worktree add -b wt/auth-refactor .worktrees/auth-refactor HEAD
    → task 12.worktree = "auth-refactor"
    → task 12.status = "in_progress"

Round 2: 在 worktree 里工作
  > worktree_run: {name: "auth-refactor", command: "ls src/"}
    → (在 .worktrees/auth-refactor/ 目录里执行)
  > worktree_run: {name: "auth-refactor", command: "cat src/auth.py"}
  > worktree_run: {name: "auth-refactor", command: "python -c 'edit auth.py...'"}

Round 3: 同时可以在另一个 worktree 里做别的
  > task_create: {subject: "修复登录 bug"}                → task 13
  > worktree_create: {name: "fix-login", task_id: 13}
  > worktree_run: {name: "fix-login", command: "..."}
  (两个 worktree 各改各的 auth.py，互不干扰)

Round 4: 收尾
  > worktree_remove: {name: "auth-refactor", complete_task: true}
    → git worktree remove .worktrees/auth-refactor
    → task 12.status = "completed"
  > worktree_keep: {name: "fix-login"}
    → worktree 保留，以后继续用
```

---

## Dispatch Map（16 个工具）

```python
TOOL_HANDLERS = {
    # Base tools (4)
    "bash", "read_file", "write_file", "edit_file",
    # Task tools (4)
    "task_create", "task_list", "task_get", "task_update",
    # Task-worktree binding (1)
    "task_bind_worktree",
    # Worktree tools (6)
    "worktree_create", "worktree_list", "worktree_status",
    "worktree_run", "worktree_keep", "worktree_remove",
    # Observability (1)
    "worktree_events",
}
```

从 s01 的 1 个工具到 s12 的 16 个工具。循环骨架从未改变。

---

## s01-s12 全景回顾

| Session | 能力 | 一句话 |
|---------|------|--------|
| **s01** | 行动 | 一个循环 + bash = agent |
| **s02** | 多工具 | dispatch map，加工具不改循环 |
| **s03** | 规划 | TodoManager，先列步骤再动手 |
| **s04** | 分工 | Subagent，大任务拆小，上下文隔离 |
| **s05** | 学知识 | Skill loading，按需加载领域知识 |
| **s06** | 管记忆 | Context compact，三层压缩保持头脑清醒 |
| **s07** | 持久化 | Task system，任务存磁盘，有依赖图 |
| **s08** | 并行 I/O | Background tasks，慢操作丢后台 |
| **s09** | 团队 | Agent teams，队友有名有姓能通信 |
| **s10** | 协议 | Team protocols，结构化请求-响应 |
| **s11** | 自治 | Autonomous agents，看板驱动自组织 |
| **s12** | 隔离 | Worktree isolation，各干各的目录 |

从一个 30 行的循环，到一个支持多 agent、任务图、worktree 隔离的完整 harness。核心循环始终是 s01 那个 `while stop_reason == "tool_use"` -- 所有后续机制都是在这个循环上叠加的。

---

## 变更总结

| 组件 | 之前（s11） | 之后（s12） |
|------|------------|------------|
| 工作目录 | 共享一个 | 每个任务独立 worktree |
| 新增类 | 无 | WorktreeManager, EventBus |
| 新增工具 | 无 | `worktree_create/list/status/run/keep/remove`, `worktree_events`, `task_bind_worktree` |
| 磁盘存储 | `.tasks/` + `.team/` | + `.worktrees/`（index.json + events.jsonl + 工作目录） |
| 状态机 | Task FSM | Task FSM + Worktree FSM |
| 崩溃恢复 | 从 .tasks/ 恢复 | 从 .tasks/ + index.json 恢复 |
| Agent loop | 不变 | 不变 |

**总结：多 agent 共享目录会互相污染。git worktree 提供目录级隔离 -- 每个任务有自己的工作目录和分支。Control plane（.tasks/）管"做什么"，Execution plane（.worktrees/）管"在哪做"，按 task_id 绑定。这是整个 harness 的最后一块拼图。**
