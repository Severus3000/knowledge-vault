# 异步（Async / Await）

`import asyncio`

只有**一个线程**，但在"等待 I/O"的间隙去干别的事。

---

## 核心关键词

| 关键词 | 含义 |
|--------|------|
| `async def` | 声明这是一个协程（coroutine），可以被暂停和恢复 |
| `await` | "我要等一个东西，等的时候让别人先跑" |
| `event loop` | 调度器，在多个协程之间切换 |
| `asyncio.gather` | 同时启动多个协程 |

---

## await 到底是什么

```
没有 await：  我发了请求 → 我傻等 → 回来了 → 继续
有 await：    我发了请求 → 告诉 event loop "我等着呢"
              → event loop 去跑别的任务
              → 回来了 → event loop 叫我继续
```

---

## Agent 场景：同时调两个 API

### 没有 async（blocking，5 秒）

```python
def handle_user_query():
    sql_result = requests.post("cloud-function/execute_sql",
                                data={"sql": "SELECT * FROM sales"})
    # ⬆️ 卡在这里，等 3 秒，什么都不干
    
    knowledge_result = requests.post("cloud-function/search_knowledge",
                                      data={"query": "沙发促销"})
    # ⬆️ 又卡在这里，等 2 秒
    # 总共等了 5 秒
```

### 用 async（3 秒，等待时间重叠）

```python
async def handle_user_query():
    sql_result, knowledge_result = await asyncio.gather(
        call_execute_sql("SELECT * FROM sales"),
        call_search_knowledge("沙发促销"),
    )
    # 总共只等 3 秒
```

### End-to-end 时间线

```
0.00s  event loop：启动 call_execute_sql()
0.01s  → 请求发出去了，遇到 await → "我在等网络，你去忙别的"

0.01s  event loop：启动 call_search_knowledge()  
0.02s  → 请求发出去了，遇到 await → "我也在等网络，你去忙别的"

       ... 两个 HTTP 请求同时在网络上飞 ...

2.00s  知识库的响应先回来了！
       event loop：call_search_knowledge，你的数据到了，继续跑 → 完成 ✓
       
3.00s  SQL 的响应回来了！  
       event loop：call_execute_sql，你的数据到了，继续跑 → 完成 ✓

3.00s  两个都完成 → combine → 返回结果（省了 2 秒）
```

---

## Event Loop 的本质

就是一个 `while True` 循环，不停地检查"有没有任务可以跑了"：

```python
# event loop 伪代码
while True:
    for task in 任务列表:
        if task.等的东西回来了:
            让 task 继续跑，直到它遇到下一个 await
    if 所有任务都完成了:
        break
```

这跟 agent 的 React 循环是同一个思想：

```
Agent React loop：循环 → 检查 LLM 有没有 tool_call → 有就执行 → 没有就退出
Event loop：      循环 → 检查网络响应有没有回来 → 有就继续跑 → 全完了就退出
```

---

## 和线程/进程的关键区别

```
线程/进程：真的有多个执行者在同时干活
async：只有一个执行者，但它很聪明 —
       "这个 API 要等 3 秒？那我先去发下一个请求，等回来了再处理"
```

async 适合**大量 I/O 等待**（网络请求、读文件）。
async 不适合 **CPU 密集型**（计算） — 只有一个线程，计算时没有"等待间隙"可以利用。

实际生产中很多 agent 框架（LangChain、OpenAI SDK）底层都是 async 的。

---

## 相关笔记

- [[concurrency-overview]] — 三种并发方式总览
- [[threading]] — 线程（多执行者方式）
- [[process]] — 进程（隔离方式）
