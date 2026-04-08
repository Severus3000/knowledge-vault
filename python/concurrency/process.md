# 进程（Process）

进程是**完全独立的执行环境**，各自有自己的内存空间。

---

## 线程 vs 进程

```
线程：同一个房间里两个人干活，共用一张桌子（快但容易抢东西）
进程：两个人在各自的房间干活，结果通过门缝递纸条（安全但传递麻烦）
```

| | 线程 | 进程 |
|--|------|------|
| 内存 | 共享 | 各自独立 |
| 通信 | 直接读写变量 | IPC（进程间通信） |
| 隔离性 | 低（一个崩全崩） | 高（一个崩不影响其他） |
| 开销 | 轻 | 重（新建整个进程） |

---

## IPC（Inter-Process Communication）

进程之间看不到彼此的变量，要传递数据需要通过 IPC：

- **stdout/stdin** — 最常用，子进程把结果写到 stdout，父进程读
- **文件** — 写到共享文件，另一个进程读
- **socket** — 网络通信
- **pipe** — 管道

---

## Agent 场景

### 子进程启动子 agent

```python
# 主 agent 启动子 agent（独立进程）
child_process = subprocess.Popen(
    ["python", "sub_agent.py", "--task", "分析红星店业绩"]
)

# 子 agent 在自己的进程里跑，有自己的内存空间
# 主 agent 看不到子 agent 里的变量

# 子 agent 跑完后，通过 stdout 把结果"传"回来 — 这就是 IPC
result = child_process.stdout.read()
```

### Claude Code 的 parallel agent

Claude Code 叫多个 agent 同时去探索代码库，就是多进程：

```
主 agent 说："探索代码库"

启动 agent A（进程1）→ 搜 src/**/*.ts
启动 agent B（进程2）→ 搜 tests/**/*.ts      同时跑
启动 agent C（进程3）→ 搜 docs/**/*.md

各自跑完，各自把结果通过 IPC 传回主 agent
主 agent 汇总三个结果，回复你
```

关键点：
- 每个 agent **互不干扰** — 一个 agent 崩了不影响其他的
- 各自**看不到彼此的变量** — 结果要通过 IPC 传回来
- 操作系统可以把不同进程分配到不同 CPU 核心上**真正并行执行**

---

## subprocess 模块

Python 启动子进程的标准方式：

```python
# 阻塞方式 — 等子进程跑完
result = subprocess.run("pytest", shell=True, capture_output=True)

# 非阻塞方式 — 启动后立刻返回
process = subprocess.Popen("pytest", shell=True)
# process 在后台跑，主进程继续
```

---

## 相关笔记

- [[concurrency-overview]] — 三种并发方式总览
- [[threading]] — 线程（共享内存的方式）
