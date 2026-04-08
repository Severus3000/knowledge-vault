# s10 - Team Protocols（团队协议）

`s01 > s02 > s03 > s04 > s05 > s06 | s07 > s08 > s09 > [ s10 ] s11 > s12`

> **核心格言**：*"队友之间要有统一的沟通规矩"* -- 多 agent 协调靠协议不靠自由文本。

---

## 问题

s09 的队友能通信了，但通信内容是**自由文本** -- `send_message("alice", "请关机")` 和 `send_message("alice", "能不能停一下")` 意思一样，但 AI 可能理解不一样。更严重的问题：

1. **关机不优雅** -- 领导想让 alice 停下来，但 alice 正在改文件改到一半。直接杀线程？文件可能写了一半。发 "请关机"？alice 可能理解成 "关电脑"。
2. **高风险操作没审批** -- alice 要删除数据库表重建，这种操作应该领导审批后再执行，而不是 alice 自己决定。

需要的是：**结构化的请求-响应协议**，不是自由文本聊天。

---

## 解决方案：Request-Response 协议

两个协议，共用同一套机制：

```
通用状态机（FSM）：pending → approved | rejected
关联方式：request_id
传递介质：JSONL 邮箱（复用 s09 的 MessageBus）
```

### 协议 1：关机协议（Shutdown）

```
Lead                              Teammate (alice)
+---------------------+          +---------------------+
| shutdown_request     |          |                     |
| {                    | -------> | 收到 shutdown 请求   |
|   request_id: "abc"  |          | 决定: 同意还是拒绝?  |
| }                    |          |                     |
+---------------------+          +-----+---------------+
                                       |
+---------------------+          +-----v---------------+
| shutdown_response    | <------- | shutdown_response   |
| {                    |          | {                   |
|   request_id: "abc"  |          |   request_id: "abc" |
|   approve: true      |          |   approve: true     |
| }                    |          | }                   |
+---------------------+          +---------------------+
         |
         v
alice 的 status → "shutdown", 线程退出
```

领导端：

```python
def handle_shutdown_request(teammate: str) -> str:
    req_id = str(uuid.uuid4())[:8]
    with _tracker_lock:
        shutdown_requests[req_id] = {"target": teammate, "status": "pending"}
    BUS.send(
        "lead", teammate, "Please shut down gracefully.",
        "shutdown_request", {"request_id": req_id},
    )
    return f"Shutdown request {req_id} sent to '{teammate}' (status: pending)"
```

队友端：

```python
if tool_name == "shutdown_response":
    req_id = args["request_id"]
    approve = args["approve"]
    with _tracker_lock:
        if req_id in shutdown_requests:
            shutdown_requests[req_id]["status"] = "approved" if approve else "rejected"
    BUS.send(
        sender, "lead", args.get("reason", ""),
        "shutdown_response", {"request_id": req_id, "approve": approve},
    )
    return f"Shutdown {'approved' if approve else 'rejected'}"
```

队友的循环里，如果 `shutdown_response` 且 `approve=True`，设置 `should_exit = True`，循环结束后 status 变成 `"shutdown"`。

关键设计：**队友有权拒绝**。如果 alice 正在写文件写到一半，她可以 `approve: false, reason: "正在写入关键文件"` 拒绝关机。领导可以等一会儿再试。

### 协议 2：计划审批（Plan Approval）

方向相反 -- 队友主动发起，领导审批：

```
Teammate (alice)                  Lead
+---------------------+          +---------------------+
| plan_approval        |          |                     |
| {                    | -------> | 收到计划            |
|   plan: "删表重建"    |          | 审查: 批准还是否决?  |
| }                    |          |                     |
+---------------------+          +-----+---------------+
                                       |
+---------------------+          +-----v---------------+
| plan_approval_resp   | <------- | plan_approval       |
| {                    |          | {                   |
|   approve: true      |          |   request_id: "xyz" |
|   feedback: "可以"    |          |   approve: true     |
| }                    |          |   feedback: "可以"   |
+---------------------+          +---------------------+
```

队友端：

```python
if tool_name == "plan_approval":
    plan_text = args.get("plan", "")
    req_id = str(uuid.uuid4())[:8]
    with _tracker_lock:
        plan_requests[req_id] = {"from": sender, "plan": plan_text, "status": "pending"}
    BUS.send(
        sender, "lead", plan_text, "plan_approval_response",
        {"request_id": req_id, "plan": plan_text},
    )
    return f"Plan submitted (request_id={req_id}). Waiting for lead approval."
```

领导端：

```python
def handle_plan_review(request_id: str, approve: bool, feedback: str = "") -> str:
    with _tracker_lock:
        req = plan_requests.get(request_id)
    req["status"] = "approved" if approve else "rejected"
    BUS.send(
        "lead", req["from"], feedback, "plan_approval_response",
        {"request_id": request_id, "approve": approve, "feedback": feedback},
    )
    return f"Plan {req['status']} for '{req['from']}'"
```

---

## 两个协议的统一模式

| 维度 | 关机协议 | 计划审批 |
|------|---------|---------|
| 发起者 | 领导 | 队友 |
| 审批者 | 队友 | 领导 |
| request_id | uuid[:8] | uuid[:8] |
| FSM | pending → approved/rejected | pending → approved/rejected |
| 传递介质 | JSONL 邮箱 | JSONL 邮箱 |
| Tracker | `shutdown_requests` 字典 | `plan_requests` 字典 |

同一套机制：
1. 生成 `request_id`，注册到 tracker（状态 = pending）
2. 通过邮箱发给对方
3. 对方处理后，通过邮箱回复（带同一个 `request_id`）
4. tracker 状态更新为 approved 或 rejected

这个模式可以扩展到**任何请求-响应场景**：代码审查、权限申请、资源分配等。只需要定义新的 `msg_type` 和对应的 handler。

---

## 队友工具集变化

```python
def _teammate_tools(self) -> list:
    return [
        bash, read_file, write_file, edit_file,  # base tools
        send_message, read_inbox,                  # from s09
        shutdown_response,                          # NEW: respond to shutdown
        plan_approval,                              # NEW: submit plan for review
    ]
```

队友新增两个工具：`shutdown_response`（响应关机请求）和 `plan_approval`（提交计划等审批）。

队友的 system prompt 也更新了：

```python
sys_prompt = (
    f"You are '{name}', role: {role}, at {WORKDIR}. "
    f"Submit plans via plan_approval before major work. "
    f"Respond to shutdown_request with shutdown_response."
)
```

明确告诉 AI：大动作前要请示，收到关机请求要回应。

---

## 领导工具集变化

```python
TOOL_HANDLERS = {
    # ... base tools + s09 tools ...
    "shutdown_request":  lambda **kw: handle_shutdown_request(kw["teammate"]),
    "shutdown_response": lambda **kw: _check_shutdown_status(kw.get("request_id", "")),
    "plan_approval":     lambda **kw: handle_plan_review(kw["request_id"], kw["approve"], ...),
}
```

领导新增三个协议工具，总计 12 个。

---

## 完整流程举例

```
Round 1: 领导 spawn alice 做数据库迁移

Round 2: alice 分析后觉得需要删表重建
  [alice] plan_approval: {plan: "删除 users 表并重建，会丢失测试数据"}
  → 发送到 lead 的收件箱

Round 3: 领导看到 alice 的计划
  > read_inbox: [{type: "plan_approval_response", from: "alice", plan: "删除 users 表..."}]
  > plan_approval: {request_id: "xyz", approve: true, feedback: "可以，测试数据无所谓"}
  → 发送审批结果到 alice 的收件箱

Round 4: alice 收到批准
  [alice] read_inbox: [{type: "plan_approval_response", approve: true, feedback: "可以..."}]
  [alice] bash: "DROP TABLE users; CREATE TABLE users..."
  [alice] send_message: {to: "lead", content: "迁移完成"}

Round 5: 领导让 alice 关机
  > shutdown_request: {teammate: "alice"}
  → "Shutdown request abc sent to 'alice' (status: pending)"

Round 6: alice 收到关机请求
  [alice] shutdown_response: {request_id: "abc", approve: true, reason: "任务已完成"}
  → alice 的线程退出，status = "shutdown"
```

---

## 变更总结

| 组件 | 之前（s09） | 之后（s10） |
|------|------------|------------|
| 通信方式 | 自由文本消息 | 自由文本 + 结构化协议 |
| 新增协议 | 无 | 关机协议、计划审批协议 |
| 新增工具 | 无 | `shutdown_request/response`, `plan_approval` |
| 状态追踪 | 无 | `shutdown_requests`, `plan_requests` 字典 |
| 队友工具 | 6 个 | 8 个（+shutdown_response, +plan_approval） |
| 领导工具 | 9 个 | 12 个（+3 个协议工具） |
| Agent loop | 不变 | 不变 |

**总结：自由文本聊天不够用。关机、审批这类操作需要结构化协议：request_id 关联请求和响应，统一 FSM（pending → approved/rejected），同一套机制可以扩展到任何请求-响应场景。**
