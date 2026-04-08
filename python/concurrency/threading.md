# 线程（Threading）

`import threading`

线程是在**同一个进程**里开多个执行路径，共享内存。

---

## 核心 API

### Thread — 创建线程

```python
thread = threading.Thread(target=要跑的函数)
```

只是**准备**了一个线程，告诉它"你的任务是这个函数"。还没开始跑。

### start() — 启动线程

```python
thread.start()   # 启动线程，立刻返回，non-blocking！
```

调用后**立刻返回**，不会等函数执行完。此刻有两个线程同时在跑：主线程和新线程。

### join() — 等待线程完成

```python
thread.join()    # blocking：卡在这里等这个线程跑完
```

`join()` = "我在这里等你完成"。是一个**汇合点** — 两条路并行走了一段，到这里必须等对方汇合才能继续。

---

## Agent 场景详解

### 不用 join（后台任务模式）

```
主 agent：开个线程跑 pytest
thread.start()
主 agent：继续处理用户消息，不管 pytest 跑没跑完
pytest 跑完后 → 结果放进 notification queue → 下轮 drain 拿到

✅ 主 agent 不阻塞
```

### 用 join（必须等结果）

```
主 agent：我要先跑 pytest，测试全过了才能 deploy

thread = Thread(target=run_pytest)
thread.start()        # 非阻塞启动
prepare_deploy()      # 同时做准备工作（并行）
thread.join()         # 准备工作做完了，现在必须等 pytest 结果

if pytest_passed:
    deploy()          # 测试过了才 deploy
```

### 对比：有线程 vs 没线程

```
没有线程（blocking）：
  主 agent 调用 pytest（要 30 秒）
  ... 30 秒啥也干不了，用户干等 ...
  pytest 跑完了
  主 agent：测试通过了！

有线程（non-blocking）：
  主 agent 开一个子线程去跑 pytest
  主 agent 立刻回复：已经在后台跑了 ✓
                                        ← 子线程：pytest 还在跑...
  用户：帮我看看 README 有没有拼写错误
  主 agent：好的，第 3 行有个 typo...      ← 主 agent 照常工作
                                        ← 子线程：pytest 跑完了！
  主 agent 收到通知：测试全部通过！
```

---

## daemon 线程

```python
thread = threading.Thread(target=run_pytest, daemon=True)
```

`daemon=True` 表示这是一个守护线程。主进程退出时，守护线程会被强制终止，不会阻止程序退出。

适合"跑完拉倒，不需要善后"的后台任务。

---

## 相关笔记

- [[concurrency-overview]] — 三种并发方式总览
- [[thread-safety]] — 线程共享内存带来的问题和解决方案
