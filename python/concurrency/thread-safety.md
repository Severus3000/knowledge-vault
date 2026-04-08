# 线程安全（Thread Safety）

线程共享内存，多个线程同时读写同一个变量会出问题。

---

## Race Condition（竞态条件）

两个线程同时操作同一个数据，结果不可预测。

### Agent 场景

主 agent 同时后台跑了 pytest 和 flake8，恰好同时跑完：

```
通知队列（notification_queue）：目前是 []

Thread A（pytest 跑完了）：
  第 1 步：读取 queue → []
  第 2 步：准备往里加 pytest_result
  第 3 步：写回 queue → [pytest_result]

Thread B（flake8 跑完了）：
  第 1 步：读取 queue → []          ← 问题！它也读到了空的 []
  第 2 步：准备往里加 flake8_result
  第 3 步：写回 queue → [flake8_result]   ← pytest 的结果被覆盖了！
```

**pytest 的结果丢了**，主 agent 永远收不到通知。

### 为什么会这样

```python
counter += 1   # 看起来是一步，其实是三步：
# 1. 读取 counter 的值（read）    → 比如是 100
# 2. 加 1（increment）            → 变成 101
# 3. 写回去（write）              → counter = 101

# 两个 thread 可能同时执行第 1 步，都读到 100，都写回 101
# 加了两次但只增了 1
```

---

## Lock / Mutex（锁 / 互斥锁）

解决 race condition：一次只让一个线程进去操作。

```python
lock = threading.Lock()    # mutex = mutual exclusion（互斥）
```

### Agent 场景

```
Thread A（pytest 跑完了）：
  with self._lock:              ← 进门，锁上
      queue.append(pytest_result)   ← 安全写入
                                ← 出门，开锁

Thread B（flake8 同时跑完了）：
  with self._lock:              ← 想进门，发现锁着的！等...

Thread A 出来了，Thread B 进去：
  with self._lock:              ← 现在可以进了，锁上
      queue.append(flake8_result)   ← 安全写入
                                ← 出门，开锁
```

结果：queue 里有 `[pytest_result, flake8_result]`，**两个都在，没丢**。

### 代码

```python
class BackgroundManager:
    def __init__(self):
        self._notification_queue = []     # 共享数据（shared state）
        self._lock = threading.Lock()     # 保护共享数据的锁

    def _execute(self, task_id, command):
        result = subprocess.run(...)      # 在 child thread 里跑
        with self._lock:                  # acquire lock
            self._notification_queue.append(result)   # 安全写入
                                          # release lock（离开 with 自动释放）
```

锁的代价：Thread B 要等 Thread A 出来。但写 queue 只要几微秒，完全可以接受。

---

## Drain（排空模式）

一次性取走队列里所有内容，清空队列。

### 为什么要 drain 而不是一个一个取

```
一个一个取：
  主 agent 取走 pytest_result → 调 LLM → 得到回复
  主 agent 取走 flake8_result → 又调 LLM → 又得到回复
  = 两次 LLM 调用，浪费 token

drain 模式：
  主 agent 一次拿走 [pytest_result, flake8_result]
  → 一起塞进 messages → 调一次 LLM
  = 一次 LLM 调用，高效
```

### 为什么 drain 也要加锁

```
不加锁：
  主 agent 正在读 queue：[pytest_result]        ← 读到 1 个
  同时 Thread B 往 queue 里加 flake8_result     ← 同时在写！
  主 agent 调 queue.clear()                     ← 清空了
  flake8_result 还没来得及被读到就被清掉了 — 丢了

加了锁：
  主 agent 锁门 → 读完 → 清空 → 开锁
  Thread B 要加东西？等主 agent 出来再加，加到下一轮 drain 里
  不会丢
```

### 代码

```python
def drain_notifications(self):
    with self._lock:                                # acquire lock
        notifs = list(self._notification_queue)     # 复制出来
        self._notification_queue.clear()            # 清空
    return notifs                                   # release lock
```

像浴缸放水：拔掉塞子 → 水全流出来 → 塞回去。

---

## 速查表

| 概念 | 一句话 |
|------|--------|
| Race Condition | 两个线程同时改一个变量，结果随机 |
| Lock / Mutex | 一次只让一个线程进去操作，排队等 |
| Drain | 一次性取走 queue 里所有东西，清空 |

---

## 相关笔记

- [[threading]] — 线程基础：start、join、daemon
- [[concurrency-overview]] — 三种并发方式总览
