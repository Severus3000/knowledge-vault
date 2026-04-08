# s07 - Task System（任务系统）

`s01 > s02 > s03 > s04 > s05 > s06 | [ s07 ] s08 > s09 > s10 > s11 > s12`

> **核心格言**：*"大目标要拆成小任务，排好序，记在磁盘上"* -- 任务比对话长命。

---

## 问题

s03 的 TodoManager 把任务存在 `messages` 列表里。两个致命缺陷：

1. **压缩后丢失** -- s06 的 auto_compact 把 messages 压缩成摘要，TodoManager 的清单也一起被压没了。AI 做了一半，压缩一次，回来就忘了自己做到哪里。
2. **扁平清单，无依赖关系** -- "先创建数据库表，再写 API，再写前端" 这种有顺序的任务，扁平清单表达不了。AI 可能跳过第一步直接写 API。

本质问题：**存在 messages 里的状态，活不过一次压缩。**

---

## 解决方案：磁盘持久化的任务图（DAG）

每个任务是一个 JSON 文件，存在 `.tasks/` 目录：

```
.tasks/
  task_1.json  {"id": 1, "subject": "创建数据库表", "status": "completed", "blockedBy": []}
  task_2.json  {"id": 2, "subject": "写 API 层",    "status": "pending",   "blockedBy": [1]}
  task_3.json  {"id": 3, "subject": "写前端页面",   "status": "pending",   "blockedBy": [1]}
  task_4.json  {"id": 4, "subject": "集成测试",     "status": "pending",   "blockedBy": [2, 3]}
```

依赖关系构成一个 **DAG**（有向无环图）：

```
                +----------+
                | task 1   |
                | 创建表    |
                | completed|
                +----+-----+
                     |
              +------+------+
              |             |
         +----v-----+  +---v------+
         | task 2   |  | task 3   |
         | 写 API   |  | 写前端   |
         | pending  |  | pending  |
         +----+-----+  +----+-----+
              |             |
              +------+------+
                     |
                +----v-----+
                | task 4   |
                | 集成测试  |
                | blocked  |
                +----------+
```

任务图回答三个问题：
- **什么可以做**：`status == "pending"` 且 `blockedBy == []`（task 2 和 task 3）
- **什么被卡住**：`blockedBy` 不为空（task 4 被 task 2 和 task 3 卡住）
- **什么做完了**：`status == "completed"`（task 1）

---

## TaskManager 类

```python
class TaskManager:
    def __init__(self, tasks_dir: Path):
        self.dir = tasks_dir
        self.dir.mkdir(exist_ok=True)
        self._next_id = self._max_id() + 1
```

初始化时扫描 `.tasks/` 目录，找到最大 ID，新任务从 `max_id + 1` 开始编号。

### CRUD 四个操作

```python
def create(self, subject: str, description: str = "") -> str:
    task = {
        "id": self._next_id, "subject": subject, "description": description,
        "status": "pending", "blockedBy": [], "owner": "",
    }
    self._save(task)
    self._next_id += 1
    return json.dumps(task, indent=2, ensure_ascii=False)

def get(self, task_id: int) -> str:
    return json.dumps(self._load(task_id), indent=2, ensure_ascii=False)

def update(self, task_id: int, status: str = None,
           add_blocked_by: list = None, remove_blocked_by: list = None) -> str:
    task = self._load(task_id)
    if status:
        task["status"] = status
        if status == "completed":
            self._clear_dependency(task_id)  # key: auto-unblock
    # ... save and return

def list_all(self) -> str:
    # Returns formatted list: [ ] #1: 创建表  [>] #2: 写 API  [x] #3: ...
```

关键方法：`_save()` 把 JSON 写到 `task_{id}.json`，`_load()` 从文件读回来。**每次操作都读写磁盘**，不缓存在内存 -- 这样即使 Python 进程重启，任务状态也不丢。

---

## blockedBy 依赖关系

核心机制在 `_clear_dependency()`：

```python
def _clear_dependency(self, completed_id: int):
    """Remove completed_id from all other tasks' blockedBy lists."""
    for f in self.dir.glob("task_*.json"):
        task = json.loads(f.read_text())
        if completed_id in task.get("blockedBy", []):
            task["blockedBy"].remove(completed_id)
            self._save(task)
```

当 task 1 完成时，扫描所有任务，把 `blockedBy` 里的 `1` 删掉。task 2 的 `blockedBy` 从 `[1]` 变成 `[]`，自动变成可执行状态。

这个设计的巧妙之处：**AI 不需要手动管理解锁**。它只需要 `update(task_id=1, status="completed")`，依赖它的任务自动被释放。

---

## Dispatch Map 加四行

```python
TOOL_HANDLERS = {
    "bash":        lambda **kw: run_bash(kw["command"]),
    "read_file":   lambda **kw: run_read(kw["path"], kw.get("limit")),
    "write_file":  lambda **kw: run_write(kw["path"], kw["content"]),
    "edit_file":   lambda **kw: run_edit(kw["path"], kw["old_text"], kw["new_text"]),
    "task_create": lambda **kw: TASKS.create(kw["subject"], kw.get("description", "")),
    "task_update": lambda **kw: TASKS.update(kw["task_id"], kw.get("status"), ...),
    "task_list":   lambda **kw: TASKS.list_all(),
    "task_get":    lambda **kw: TASKS.get(kw["task_id"]),
}
```

四个任务工具，四行 dispatch map。循环不变。

---

## 跟 s03 的区别

| 维度 | s03 TodoManager | s07 TaskManager |
|------|----------------|-----------------|
| 存储位置 | 内存（messages 列表） | 磁盘（.tasks/ 目录） |
| 结构 | 扁平清单 | DAG（有依赖关系） |
| 压缩后 | 丢失 | 不受影响 |
| 进程重启后 | 丢失 | 从文件恢复 |
| 自动解锁 | 无 | _clear_dependency |

一句话概括：**s03 的任务活在对话里，s07 的任务活在文件系统里。**

---

## 完整流程举例

用户说："帮我重构认证模块，分步骤来"

```
Round 1:
  AI 创建任务：
  > task_create: {subject: "分析现有认证代码"}          → task_1.json
  > task_create: {subject: "设计新认证接口"}            → task_2.json
  > task_create: {subject: "实现新认证逻辑"}            → task_3.json
  > task_create: {subject: "写单元测试"}                → task_4.json
  > task_update: {task_id: 2, addBlockedBy: [1]}       → task 2 等 task 1
  > task_update: {task_id: 3, addBlockedBy: [2]}       → task 3 等 task 2
  > task_update: {task_id: 4, addBlockedBy: [3]}       → task 4 等 task 3

Round 2-5:
  AI 完成 task 1 → update(1, status="completed")
  → _clear_dependency(1) → task 2 的 blockedBy 变成 []
  AI 自动开始 task 2...

  [中途触发 auto_compact，messages 被压缩]

Round 6:
  AI 压缩后只看到摘要，但调用 task_list 就能恢复全貌：
  > task_list:
    [x] #1: 分析现有认证代码
    [x] #2: 设计新认证接口
    [>] #3: 实现新认证逻辑
    [ ] #4: 写单元测试 (blocked by: [3])

  AI 知道自己做到哪里了，继续 task 3。
```

---

## 任务图是 s08-s12 的协调骨架

从 s07 开始，`.tasks/` 目录成为后续所有 session 的核心数据结构：

| Session | 怎么用任务图 |
|---------|-------------|
| **s08** | 后台任务完成后更新 task 状态 |
| **s09** | 队友从任务图里领活 |
| **s10** | 计划审批针对某个 task |
| **s11** | 自治 agent 扫描看板自动认领 unclaimed task |
| **s12** | 每个 task 绑定一个 worktree |

任务图是**协调的骨架**，后面的机制都围绕它构建。

---

## 变更总结

| 组件 | 之前（s06） | 之后（s07） |
|------|------------|------------|
| 任务管理 | 内存中的 TodoManager | 磁盘持久化的 TaskManager |
| 新增工具 | 无 | `task_create`, `task_update`, `task_list`, `task_get` |
| 磁盘存储 | `.transcripts/` | `.transcripts/` + `.tasks/` |
| 依赖关系 | 无 | `blockedBy` 字段 + `_clear_dependency()` |
| Agent loop | 不变 | 不变 |

**总结：任务比对话长命。存在磁盘上的任务图，不怕压缩、不怕重启、有依赖关系、能自动解锁 -- 这是从"对话内规划"到"持久化协调"的关键一步。**
