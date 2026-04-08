# 深度学习计划：Agent 框架背后的 CS 基础

> 目标：把 learn-claude-code 12 个 session 涉及的每个知识点吃透
> 前置：12 个 session 全部完成，已有 [[concurrency-overview]]、[[async-await]]、[[threading]]、[[process]]、[[thread-safety]] 笔记
> 方法：每个模块先理解原理，再读源码，最后关联回 agent 场景

---

## 模块总览

| # | CS 基础 | 对应 Session | 核心问题 |
|---|---------|-------------|---------|
| 1 | Event Loop & 协程原理 | s01, s08 | while True 循环怎么实现并发的？ |
| 2 | IPC 进程间通信 | s09, s10 | agent 之间怎么通信？文件 vs 管道 vs socket |
| 3 | DAG 与任务调度 | s07, s11 | 有依赖的任务怎么排序和并行？ |
| 4 | 缓存与内存管理 | s06 | 上下文压缩本质是什么淘汰策略？ |
| 5 | 插件与动态加载 | s05 | skill 按需加载背后的 Python 机制 |
| 6 | 进程隔离与沙箱 | s04, s12 | 子 agent 的隔离到底隔了什么？ |
| 7 | 状态机 | s11 | WORK/IDLE 状态转换的形式化模型 |
| 8 | 并发模式 | s08-s12 | fan-out、supervisor、worker pool |

---

## 模块 1：Event Loop & 协程原理

**已有知识**：知道 event loop 是 while True + 检查任务，知道 await 让出控制权
**深入方向**：从零实现一个 event loop，理解 generator → coroutine → asyncio 的演进

### 学习资源

| 资源 | 说明 |
|------|------|
| [AndreLouisCaron/a-tale-of-event-loops](https://github.com/AndreLouisCaron/a-tale-of-event-loops) ⭐331 | 深入笔记：Python event loop 内部原理，`.send()`、coroutine 执行、timer、I/O polling |
| [How on earth does Asyncio work](https://gist.github.com/dvf/cc11392a0bd74726de4ec8a6e7be971c) | 从 generator 开始手写一个 event loop，一步步到 asyncio |
| [CPython Lib/asyncio/](https://github.com/python/cpython/tree/main/Lib/asyncio) | 读 `tasks.py`（TaskGroup）、`events.py`（event loop 接口）、`selector_events.py`（I/O 多路复用） |
| [econchick/mayhem](https://github.com/econchick/mayhem) ⭐303 | 生产级 asyncio 模式：queue、signal handling、graceful shutdown |

### 关联回 agent

```
s01 agent loop:  while stop_reason == "tool_use"  ← 最简单的 event loop
s08 background:  asyncio.create_task()            ← 真正的 event loop 调度
```

### 深入问题
- [ ] generator 的 `.send()` 和 `yield` 怎么实现协程切换？
- [ ] `select/poll/epoll/kqueue` 有什么区别？Python 用哪个？
- [ ] asyncio 的 TaskGroup 和 gather 有什么区别？什么时候用哪个？

---

## 模块 2：IPC 进程间通信

**已有知识**：知道 s09 用 JSONL 文件作邮箱，drain-on-read 模式
**深入方向**：理解所有 IPC 方式的 trade-off，为什么文件是"最可靠的"

### 学习资源

| 资源 | 说明 |
|------|------|
| [spurin/python-ipc-examples](https://github.com/spurin/python-ipc-examples) | 全面覆盖：pipe、named pipe、socket（domain + TCP）、message queue、shared memory |
| [djeada/Parallel-And-Concurrent-Programming](https://github.com/djeada/Parallel-And-Concurrent-Programming) | IPC + 并发完整课程，Python/C++/JS 对比 |
| OSTEP Ch.5 (Process API) + Ch.30-33 | 管道、信号、锁的 OS 层面解释 |

### 关联回 agent

```
s09 MessageBus:  JSONL 文件 ← 最简单的 IPC
s10 protocols:   请求-响应格式 ← 序列化协议
生产级:          WebSocket / gRPC / Redis Pub/Sub
```

### 深入问题
- [ ] pipe 是单向的，怎么实现双向通信？
- [ ] Unix domain socket vs TCP socket 什么区别？
- [ ] 为什么 s09 用文件而不用 `multiprocessing.Queue`？trade-off 是什么？
- [ ] 生产环境的 agent 通信通常用什么？（Redis、NATS、Kafka？）

---

## 模块 3：DAG 与任务调度

**已有知识**：知道 s07 用 JSON 文件表示 blockedBy 依赖
**深入方向**：拓扑排序算法，任务调度器的设计

### 学习资源

| 资源 | 说明 |
|------|------|
| [thieman/dagobah](https://github.com/thieman/dagobah) ⭐766 | Python DAG job scheduler，有 web UI，dependency graph |
| [mindee/tawazi](https://github.com/mindee/tawazi) ⭐90 | 用装饰器声明 DAG 依赖，自动并行化执行 |
| [intzeros/parallel-task-graph](https://github.com/intzeros/parallel-task-graph) | 核心算法 ~200 行：拓扑排序 + 线程池执行 |

### 关联回 agent

```
s07 task system:  blockedBy: [1, 2] ← 就是 DAG 的边
s11 autonomous:   claim_task 看板 ← 就是 work-stealing 调度
Airflow/Prefect:  生产级 DAG 调度器
```

### 深入问题
- [ ] Kahn's algorithm vs DFS 拓扑排序有什么区别？
- [ ] 如果 DAG 有环（循环依赖）怎么检测？
- [ ] 任务调度的 work-stealing 是什么？和 s11 的 claim_task 什么关系？

---

## 模块 4：缓存与内存管理

**已有知识**：知道 s06 三层压缩（micro_compact / auto_compact / compact 工具）
**深入方向**：这些策略背后是什么 CS 概念

### 学习资源

| 资源 | 说明 |
|------|------|
| [tkem/cachetools](https://github.com/tkem/cachetools) ⭐2.7k | LRU、LFU、TTL、Random Replacement 全实现，Python 源码可读 |
| [jlhutch/pylru](https://github.com/jlhutch/pylru) ⭐222 | 纯 Python LRU：HashMap + 双向链表，O(1) 查找 + 淘汰 |
| [ashishps1/awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design) ⭐23k | LRU Cache 完整设计 + 数十种系统设计模式 |

### 关联回 agent

```
s06 micro_compact:  替换旧 tool_result ← 类似 LRU（最旧的先淘汰）
s06 auto_compact:   摘要替换全部     ← 类似 cache flush + summary
LLM context:        sliding window   ← 滑动窗口算法
```

### 深入问题
- [ ] LRU vs LFU 什么区别？s06 的压缩更像哪个？
- [ ] 为什么 s06 选择"摘要替换"而不是"直接丢弃"？信息论角度怎么看？
- [ ] 生产 agent 的 context management 有哪些策略？（RAG、summarize、truncate）

---

## 模块 5：插件与动态加载

**已有知识**：知道 s05 把 skill 目录放 system prompt，正文按需加载
**深入方向**：Python 的动态导入机制，注册表模式

### 学习资源

| 资源 | 说明 |
|------|------|
| [mitsuhiko/pluginbase](https://github.com/mitsuhiko/pluginbase) ⭐1.1k | Flask 作者写的插件系统，隔离的插件上下文 + 动态加载 |
| [localstack/plux](https://github.com/localstack/plux) ⭐75 | PluginSpec → init → loaded 生命周期，基于 Python entry points |
| Python docs: `importlib` | `importlib.import_module()` 和 `__init_subclass__` 自注册模式 |

### 关联回 agent

```
s05 skill:        目录在 system prompt, load_skill 工具按需读文件
VS Code:          extension manifest (package.json) + activate()
Claude Code:      skills/ 目录 + Skill tool
```

### 深入问题
- [ ] Python 的 `importlib` 怎么实现动态加载？和 `__import__` 什么关系？
- [ ] 注册表模式（Registry Pattern）怎么用装饰器实现？
- [ ] 懒加载（lazy loading）在 agent 场景有什么好处？

---

## 模块 6：进程隔离与沙箱

**已有知识**：知道 s04 子 agent 有独立 messages，s12 用 git worktree 隔离文件
**深入方向**：隔离的本质是什么？OS 层面怎么实现？

### 学习资源

| 资源 | 说明 |
|------|------|
| [Fewbytes/rubber-docker](https://github.com/Fewbytes/rubber-docker) ⭐3.2k | **强推。** 用 Python 从零重建 Docker：chroot → mount namespace → overlay FS → cgroups |
| [google/nsjail](https://github.com/google/nsjail) ⭐3.8k | Google 的隔离工具，README 是 namespace/cgroup/seccomp 的最佳入门 |

### 关联回 agent

```
s04 subagent:     messages 隔离 ← 应用层隔离（最轻量）
s12 worktree:     文件系统隔离 ← git worktree = 轻量级 chroot
Docker:           全面隔离（namespace + cgroup + overlay FS）
```

### 深入问题
- [ ] chroot 和 namespace 有什么区别？
- [ ] Docker 的隔离和虚拟机的隔离有什么本质区别？
- [ ] agent 的隔离需要到什么程度？内存隔离 vs 文件隔离 vs 网络隔离？

---

## 模块 7：状态机

**已有知识**：知道 s11 的 WORK → IDLE → WORK 循环
**深入方向**：有限状态机的形式化定义，状态图

### 学习资源

| 资源 | 说明 |
|------|------|
| [pytransitions/transitions](https://github.com/pytransitions/transitions) ⭐6.5k | 最流行的 Python FSM 库，README 就是一个完整教程（从 2 状态到嵌套层次状态） |
| [fgmacedo/python-statemachine](https://github.com/fgmacedo/python-statemachine) ⭐1.2k | 现代 statecharts：复合状态、并行区域、历史状态 |
| [alysivji/finite-state-machine](https://github.com/alysivji/finite-state-machine) ⭐113 | ~100 行实现 FSM，用装饰器定义状态转换 |

### 关联回 agent

```
s11 agent:     WORK → IDLE → WORK（简单 FSM）
HTTP:          CONNECTING → OPEN → CLOSING → CLOSED（WebSocket 状态机）
TCP:           经典 11 状态状态机
```

### 深入问题
- [ ] 有限状态机（FSM）和状态图（Statechart）有什么区别？
- [ ] 状态爆炸问题怎么解决？层次状态机怎么帮忙？
- [ ] agent 的状态应该用代码枚举还是用状态机库管理？

---

## 模块 8：并发模式

**已有知识**：知道 fan-out、线程、进程的概念
**深入方向**：系统化学习所有并发模式

### 学习资源

| 资源 | 说明 |
|------|------|
| [python-trio/trio](https://github.com/python-trio/trio) ⭐7.2k | Structured concurrency 鼻祖，设计文档比代码更值得读 |
| [agronholm/anyio](https://github.com/agronholm/anyio) ⭐2.4k | TaskGroup + 取消 + capacity limiter，MCP SDK 依赖它 |
| [djeada/Parallel-And-Concurrent-Programming](https://github.com/djeada/Parallel-And-Concurrent-Programming) | 全课程：mutex、semaphore、barrier、reader-writer lock、producer-consumer |

### 关联回 agent

```
Fan-out/Fan-in:    s09 spawn 多个 teammate → 收集结果
Supervisor:        s09 领导监控队友状态
Worker pool:       s11 自治 agent 从看板 claim task
Producer-Consumer: s09 MessageBus（send = produce, read_inbox = consume）
```

### 深入问题
- [ ] Structured concurrency 和普通并发有什么根本区别？
- [ ] Erlang 的 supervisor tree 是什么？和 agent 架构有什么关系？
- [ ] 背压（backpressure）是什么？当 agent 产出速度 > 消费速度怎么办？

---

## 学习顺序建议

```
模块 1（Event Loop）→ 模块 8（并发模式）→ 模块 2（IPC）
    ↓
模块 3（DAG）→ 模块 7（状态机）
    ↓
模块 4（缓存）→ 模块 5（插件）→ 模块 6（隔离）
```

先理解底层执行模型（event loop + 并发），再理解通信和调度（IPC + DAG），最后理解工程模式（缓存 + 插件 + 隔离）。

---

## 相关笔记

- [[concurrency-overview]] — 三种并发方式总览
- [[async-await]] — 异步基础
- [[threading]] — 线程
- [[process]] — 进程
- [[thread-safety]] — 竞态条件与锁
