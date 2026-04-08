# s09 - Agent Teams（Agent 团队）

`s01 > s02 > s03 > s04 > s05 > s06 | s07 > s08 > [ s09 ] s10 > s11 > s12`

> **核心格言**：*"任务太大一个人干不完，要能分给队友"* -- 多 agent 靠文件通信不靠共享内存。

---

## 问题

之前有两种"分工"机制，都不够：

1. **s04 Subagent** -- 一次性的。启动 → 执行 → 返回摘要 → 销毁。没有生命周期，不能持续工作，不能和其他 agent 通信。类比：叫了个外卖员，送完就走了。
2. **s08 Background** -- 只能跑 shell 命令，没有 LLM 思考能力。`background_run("npm install")` 可以，但 `background_run("分析这段代码的性能瓶颈")` 不行 -- 它没有 AI 大脑。

需要的是：**有名字、有角色、能持续工作、能互相通信的队友**。类比：雇正式员工，有工位有邮箱，不是叫外卖的。

---

## 两个核心组件

### 1. TeammateManager -- 管人

```python
class TeammateManager:
    def __init__(self, team_dir: Path):
        self.dir = team_dir
        self.config_path = self.dir / "config.json"  # team roster
        self.config = self._load_config()
        self.threads = {}  # name -> Thread
```

配置文件 `.team/config.json` 存储团队花名册：

```json
{
  "team_name": "default",
  "members": [
    {"name": "alice", "role": "coder", "status": "working"},
    {"name": "bob",   "role": "tester", "status": "idle"}
  ]
}
```

#### spawn() -- 创建队友

```python
def spawn(self, name: str, role: str, prompt: str) -> str:
    member = {"name": name, "role": role, "status": "working"}
    self.config["members"].append(member)
    self._save_config()
    thread = threading.Thread(
        target=self._teammate_loop,
        args=(name, role, prompt),
        daemon=True,
    )
    self.threads[name] = thread
    thread.start()
    return f"Spawned '{name}' (role: {role})"
```

每个队友在**独立线程**里跑自己的 agent loop。有自己的 `messages` 列表、自己的 system prompt、自己的工具集。

#### 队友的生命周期

```
spawn("alice", "coder", "实现用户认证模块")
  |
  v
WORKING -- alice 在自己的线程里跑 agent loop
  |         调用 bash、read_file、write_file...
  |         每轮循环前检查收件箱
  |
  | stop_reason != "tool_use" (LLM 觉得做完了)
  v
IDLE -- alice 闲了，等待新指令
  |
  | 收到新消息 → 回到 WORKING
  | 收到 shutdown_request → SHUTDOWN
  v
SHUTDOWN -- alice 退出
```

跟 s04 subagent 的关键区别：**subagent 做完就销毁，teammate 做完变 IDLE，还在那里等新任务。**

### 2. MessageBus -- 管信

```python
class MessageBus:
    def __init__(self, inbox_dir: Path):
        self.dir = inbox_dir  # .team/inbox/

    def send(self, sender: str, to: str, content: str,
             msg_type: str = "message", extra: dict = None) -> str:
        msg = {
            "type": msg_type,
            "from": sender,
            "content": content,
            "timestamp": time.time(),
        }
        inbox_path = self.dir / f"{to}.jsonl"
        with open(inbox_path, "a") as f:
            f.write(json.dumps(msg) + "\n")
        return f"Sent {msg_type} to {to}"

    def read_inbox(self, name: str) -> list:
        inbox_path = self.dir / f"{name}.jsonl"
        if not inbox_path.exists():
            return []
        messages = [json.loads(l) for l in inbox_path.read_text().strip().splitlines() if l]
        inbox_path.write_text("")  # drain-on-read
        return messages
```

每个队友有一个 JSONL 文件作为收件箱：

```
.team/inbox/
  alice.jsonl
  bob.jsonl
  lead.jsonl
```

通信机制：
- **send()** -- 往对方的 `.jsonl` 文件追加一行（`"a"` 模式）
- **read_inbox()** -- 读取所有行，然后**清空文件**（drain-on-read）
- **broadcast()** -- 给所有队友发消息（循环调用 send）

为什么用文件而不用队列/共享内存？因为**文件是最可靠的 IPC 机制** -- 进程崩溃了消息不丢，重启后还在。

---

## 队友的循环

```python
def _teammate_loop(self, name: str, role: str, prompt: str):
    sys_prompt = (
        f"You are '{name}', role: {role}, at {WORKDIR}. "
        f"Use send_message to communicate. Complete your task."
    )
    messages = [{"role": "user", "content": prompt}]
    tools = self._teammate_tools()

    for _ in range(50):  # safety limit
        # Check inbox before each LLM call
        inbox = BUS.read_inbox(name)
        for msg in inbox:
            messages.append({"role": "user", "content": json.dumps(msg)})

        response = client.messages.create(
            model=MODEL, system=sys_prompt, messages=messages,
            tools=tools, max_tokens=8000,
        )
        messages.append({"role": "assistant", "content": response.content})
        if response.stop_reason != "tool_use":
            break
        # ... execute tools, append results
    # Loop done → status = "idle"
```

仔细看 -- 这就是 s01 的 agent loop，加了两个特性：
1. **每轮开始前检查收件箱**，有消息就注入 messages
2. **独立的 system prompt**，告诉 AI 它的名字和角色

队友拥有的工具：

```python
def _teammate_tools(self) -> list:
    return [
        bash, read_file, write_file, edit_file,  # base tools from s02
        send_message,  # communicate with teammates
        read_inbox,    # check own inbox
    ]
```

注意：队友**没有 spawn_teammate 工具** -- 只有领导能创建队友（防止无限增殖，和 s04 子 agent 不能再生子 agent 是同一个思路）。

---

## 领导的 Dispatch Map

```python
TOOL_HANDLERS = {
    "bash":            lambda **kw: _run_bash(kw["command"]),
    "read_file":       lambda **kw: _run_read(kw["path"], kw.get("limit")),
    "write_file":      lambda **kw: _run_write(kw["path"], kw["content"]),
    "edit_file":       lambda **kw: _run_edit(kw["path"], kw["old_text"], kw["new_text"]),
    "spawn_teammate":  lambda **kw: TEAM.spawn(kw["name"], kw["role"], kw["prompt"]),
    "list_teammates":  lambda **kw: TEAM.list_all(),
    "send_message":    lambda **kw: BUS.send("lead", kw["to"], kw["content"]),
    "read_inbox":      lambda **kw: json.dumps(BUS.read_inbox("lead"), indent=2),
    "broadcast":       lambda **kw: BUS.broadcast("lead", kw["content"], TEAM.member_names()),
}
```

9 个工具。领导比队友多了 `spawn_teammate`、`list_teammates`、`broadcast` 三个管理工具。

---

## s04 vs s09 对比

| 维度 | s04 Subagent | s09 Teammate |
|------|-------------|--------------|
| 生命周期 | 一次性，做完即销毁 | 持久化，做完变 IDLE |
| 通信方式 | 无（只返回摘要给主 agent） | JSONL 邮箱双向通信 |
| 身份 | 匿名 | 有名字、角色 |
| 状态持久化 | 无 | `.team/config.json` |
| 类比 | 叫外卖员，送完就走 | 雇正式员工，有工位有邮箱 |

---

## 完整流程举例

用户说："帮我实现登录功能，需要后端 API 和前端页面"

```
Round 1:
  领导 AI 思考：这需要两个人同时干
  > spawn_teammate: {name: "alice", role: "backend", prompt: "实现 /api/login 接口"}
  > spawn_teammate: {name: "bob", role: "frontend", prompt: "实现登录页面 UI"}

  alice 线程启动：
    messages = [{role: "user", content: "实现 /api/login 接口"}]
    → bash: cat routes/auth.py
    → edit_file: 添加 login route
    → send_message: {to: "bob", content: "API 接口是 POST /api/login, 参数: email, password"}
    → send_message: {to: "lead", content: "后端接口已完成"}

  bob 线程启动：
    messages = [{role: "user", content: "实现登录页面 UI"}]
    → read_inbox: [{"from": "alice", "content": "API 接口是 POST /api/login..."}]
    → write_file: 创建 login.html
    → send_message: {to: "lead", content: "前端页面已完成，已对接 alice 的 API"}

Round 2:
  领导 AI 检查收件箱：
  > read_inbox:
    [{"from": "alice", "content": "后端接口已完成"},
     {"from": "bob", "content": "前端页面已完成，已对接 alice 的 API"}]

  领导回复用户："登录功能已完成。alice 实现了后端 API，bob 实现了前端页面。"
```

注意：alice 和 bob **直接通信**（alice 发 API 信息给 bob），不需要领导中转。这是 s04 subagent 做不到的。

---

## 变更总结

| 组件 | 之前（s08） | 之后（s09） |
|------|------------|------------|
| Agent 架构 | 单 agent + 后台线程 | 领导 + N 个队友（各自有完整 agent loop） |
| 新增类 | 无 | TeammateManager, MessageBus |
| 通信方式 | 无 | JSONL 邮箱（.team/inbox/） |
| 新增工具 | 无 | `spawn_teammate`, `list_teammates`, `send_message`, `read_inbox`, `broadcast` |
| 状态持久化 | 无 | `.team/config.json` |
| Agent loop | 领导不变，队友各有自己的循环 | 循环前检查收件箱 |

**总结：队友不是一次性的外卖员，而是有名有姓的正式员工。他们在独立线程里跑完整的 agent loop，通过 JSONL 邮箱互相通信。领导管人（spawn/list），邮局管信（send/read）。**
