# Generator / yield

Generator 是一种特殊的函数，用 `yield` 一个一个吐出值，而不是一次性返回全部。

---

## 普通函数 vs Generator

```python
# 普通函数：一次性算完，全部返回
def get_numbers():
    result = []
    for i in range(5):
        result.append(i)
    return result          # 返回 [0, 1, 2, 3, 4]

numbers = get_numbers()    # 内存里一次性存了整个列表
```

```python
# generator：一个一个吐，用一个算一个
def get_numbers():
    for i in range(5):
        yield i            # 吐出一个，暂停，等别人来拿下一个

for n in get_numbers():    # 每次循环，generator 才算下一个
    print(n)               # 0, 1, 2, 3, 4
```

**`yield` = "给你一个，我先暂停，你要下一个的时候我再继续"**

---

## yield 的暂停/恢复机制

这是 generator 最核心的特性：

```python
def count():
    print("开始")
    yield 1          # 吐出 1，暂停在这里
    print("继续")
    yield 2          # 吐出 2，暂停在这里
    print("结束")
    yield 3          # 吐出 3，暂停在这里

gen = count()        # 什么都没发生！函数没有执行
```

```
next(gen)    →  打印 "开始"，返回 1，暂停
next(gen)    →  打印 "继续"，返回 2，暂停
next(gen)    →  打印 "结束"，返回 3，暂停
next(gen)    →  StopIteration（没了）
```

`for chunk in stream` 底层就是不停调 `next()`，每次拿一个值，直到 generator 结束。

---

## Agent 场景：LLM 流式输出

bot 调 LLM，LLM 生成回复需要 5 秒。

### 非流式（普通函数模式）

```
用户：红星店这个月业绩怎么样？

0s   agent 调 LLM API
...  用户看到"正在输入..."，干等 5 秒
5s   LLM 生成完毕，一次性返回完整回复
     agent 发给用户："红星店本月销售额 28 万，环比上涨 12%..."

用户体验：干等 5 秒，然后一大段文字突然出现
```

```python
response = client.messages.create(
    model="qwen/qwen3-plus",
    messages=messages,
    max_tokens=1000,
)
# response 是完整的回复，5 秒后才拿到
print(response.content[0].text)   # 一次性全打出来
```

### 流式（generator 模式）

```
用户：红星店这个月业绩怎么样？

0.0s  agent 调 LLM API（stream=True）
0.3s  LLM 吐出 "红星"        → 立刻发给用户
0.5s  LLM 吐出 "店本月"      → 立刻发给用户
0.8s  LLM 吐出 "销售额"      → 立刻发给用户
1.0s  LLM 吐出 "28万"        → 立刻发给用户
...
5.0s  LLM 吐完

用户体验：0.3 秒就看到第一个字，文字一个一个蹦出来
```

```python
stream = client.messages.create(
    model="qwen/qwen3-plus",
    messages=messages,
    max_tokens=1000,
    stream=True,              # 关键：开启流式
)
# stream 是一个 generator，每次 yield 一小块

for chunk in stream:          # 每次循环拿到一小块
    if chunk.type == "content_block_delta":
        print(chunk.delta.text, end="")   # 一个字一个字打出来
```

---

## 为什么不用列表而用 Generator

### 内存

```python
# 列表方式：10000 个 token 全部存在内存里
tokens = get_all_tokens()     # 内存占用：10000 个 token

# generator 方式：内存里同一时间只有 1 个 token
for token in get_tokens():    # 内存占用：1 个 token
    send_to_user(token)       # 用完就扔，拿下一个
```

### 延迟（对 agent 更重要）

- 列表：用户等 5 秒才看到第一个字
- Generator：用户 0.3 秒就看到第一个字

---

## 实际应用：WeCom bot 流式回复

```python
def handle_message(user_query):
    stream = client.messages.create(
        model=MODEL,
        messages=[{"role": "user", "content": user_query}],
        stream=True,
    )
    
    buffer = ""
    for chunk in stream:                           # generator，一块一块来
        if chunk.type == "content_block_delta":
            buffer += chunk.delta.text
            if len(buffer) > 50:                   # 攒够 50 个字发一次
                send_to_wecom(user_id, buffer)     # 发给用户
                buffer = ""
    
    if buffer:                                     # 发剩余的
        send_to_wecom(user_id, buffer)
```

用户不用干等，文字一段一段出现。

---

## 相关笔记

- [[concurrency/async-await]] — async generator 结合异步使用
- [[decorator]] — 装饰器（另一个 agent 开发常用概念）
