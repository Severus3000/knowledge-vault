# Exception Handling（异常处理）

程序出错时不崩溃，优雅地处理问题继续运行。

---

## 基本语法

### try / except — 接住崩溃

```python
try:
    result = 10 / 0                # 可能出错的代码放这里
except ZeroDivisionError as e:     # 如果出了这种错，走这里
    print(f"出错了：{e}")           # 打印：出错了：division by zero

print("程序没崩，继续跑")           # 这行正常执行
```

**`try` = "试试看"，`except` = "如果出错了怎么办"。**

`10 / 0` 这个例子每次都会走 except（必定出错），但重点是：有了 try/except 程序**不会崩**。它走 except 打印错误信息，然后继续往下执行 `print("程序没崩，继续跑")`。

try/except 的意思不是"防止错误发生"，而是"错误发生了我接住它，程序别死"。

### try 里多行代码的执行规则

try 里可以放多行代码，规则是：**从上往下执行，哪一行出错就立刻跳到 except，后面的行不执行。**

```python
def execute_sql(sql):
    try:
        response = requests.post(URL, json={"sql": sql}, timeout=10)  # 第 1 行
        response.raise_for_status()                                     # 第 2 行
        return response.json()                                          # 第 3 行
    except requests.Timeout:
        return "错误：查询超时"
    except requests.HTTPError as e:
        return f"错误：服务器返回 {e.response.status_code}"
    except Exception as e:
        return f"错误：{e}"
```

**情况 1：第一行就崩了（网络超时）**
```
response = requests.post(...)     # 💥 超时！
response.raise_for_status()       # 跳过
return response.json()            # 跳过
→ 走 except requests.Timeout
```

**情况 2：第一行过了，第二行崩了（服务器返回 500）**
```
response = requests.post(...)     # ✅ 请求发出去了
response.raise_for_status()       # 💥 状态码 500，抛异常！
return response.json()            # 跳过
→ 走 except requests.HTTPError
```

**情况 3：三行都过了**
```
response = requests.post(...)     # ✅ 请求成功
response.raise_for_status()       # ✅ 状态码 200
return response.json()            # ✅ 返回结果
→ 不走任何 except
```

不是"所有行都要过才能过"——是**逐行执行，出错的那一行决定走哪个 except**。

### finally — 不管成不成功都要做的事

```python
def query_database(sql):
    conn = db.connect()              # 打开[[database/connection|数据库连接]]
    try:
        result = conn.execute(sql)
        return result
    except Exception as e:
        print(f"查询失败：{e}")
        return None
    finally:
        conn.close()                 # 不管成功还是失败，都要关连接
```

**`finally` = "不管怎样都执行"。** 用来清理资源（关连接、关文件）。

为什么需要 finally？因为[[database/connection|数据库连接]]是有限资源——打开了必须关掉，不然连接会越积越多，最终数据库被占满。如果把 `conn.close()` 写在 try 里面，一旦出错就跳到 except 了，close 不会执行。`finally` 保证它一定跑。

### raise — 主动抛异常

两种用法：

**1. 主动创建一个新错误**

```python
def execute_sql(sql):
    if "DROP" in sql.upper() or "DELETE" in sql.upper():
        raise ValueError("不允许执行破坏性 SQL！")    # 主动崩，阻止危险操作
    return db.query(sql)
```

bot 是只读的，如果 LLM 生成了 DELETE 语句，应该主动 raise 拒绝掉，让上层的 try/except 接住返回友好提示。

**2. 在 except 里原样再抛出**

```python
except Exception as e:
    if attempt == max_attempts - 1:
        raise       # 把刚才接住的错误原样扔出去
```

单独写 `raise` 不带任何东西 = "我接住看了一眼，还是决定让它崩"。在 [[decorator#带参数的 Decorator（三层嵌套）|retry decorator]] 里用来表示"重试机会用完了，报错吧"。

---

## 异常的层级

Python 的异常有继承关系，像一棵树：

```
Exception（所有异常的爸爸）
├── requests.RequestException
│   ├── requests.Timeout          ← 超时
│   ├── requests.ConnectionError  ← 连不上
│   └── requests.HTTPError        ← 服务器返回错误码
├── json.JSONDecodeError          ← JSON 解析失败
├── KeyError                      ← [[dictionary|dict]] 里找不到 key
└── ValueError                    ← 值不对
```

```python
try:
    ...
except requests.Timeout:           # 只接住超时
    ...
except requests.RequestException:   # 接住所有网络相关错误
    ...
except Exception:                   # 接住一切（兜底）
    ...
```

**从具体到笼统排列**。Python 从上往下匹配，匹配到第一个就停。

每个 except 对应的不是"某一行代码"，而是"某一类错误"。try 里不管哪一行抛出的错误，都会从上到下去匹配 except。

如果把 `Exception` 放第一个，所有错误都被它接住了，后面的具体 except 永远不会执行。所以**具体的放前面，兜底的放最后**。

---

## Agent 场景：API 调用

### 不处理异常 — 一个请求失败，整个 bot 崩掉

```python
def execute_sql(sql):
    response = requests.post(URL, json={"sql": sql}, timeout=10)
    return response.json()

# 网络超时？→ bot 崩了
# 服务器 500？→ bot 崩了
# 返回的不是 JSON？→ bot 崩了
```

### 处理异常 — 失败了优雅处理，bot 继续运行

```python
def execute_sql(sql):
    try:
        response = requests.post(URL, json={"sql": sql}, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.Timeout:
        return "错误：查询超时，请稍后再试"
    except requests.HTTPError as e:
        return f"错误：服务器返回 {e.response.status_code}"
    except Exception as e:
        return f"错误：{e}"
```

用户看到的是"查询超时，请稍后再试"，而不是 bot 直接断线。

---

## Agent 场景：分层错误处理

实际 agent 里，错误处理分好几层：

```python
# 第 1 层：工具函数里 — 处理具体的技术错误
def execute_sql(sql):
    try:
        response = requests.post(URL, json={"sql": sql}, timeout=10)
        return response.json()["data"]
    except requests.Timeout:
        raise ToolError("数据库查询超时")     # 转成工具层面的错误，往上抛
    except requests.HTTPError:
        raise ToolError("后端服务异常")

# 第 2 层：dispatch 里 — 处理工具调用的错误
def dispatch_tool(tool_name, tool_args):
    try:
        handler = TOOL_REGISTRY[tool_name]
        return {"status": "success", "result": handler(**tool_args)}
    except ToolError as e:
        return {"status": "error", "result": str(e)}
    except KeyError:
        return {"status": "error", "result": f"未知工具：{tool_name}"}

# 第 3 层：agent loop 里 — 兜底，保证 bot 永远不崩
def agent_loop(messages):
    while True:
        try:
            response = client.messages.create(...)
            # ... 处理 tool_calls ...
        except Exception as e:
            print(f"[FATAL] agent loop 异常：{e}")
            messages.append({
                "role": "assistant",
                "content": "抱歉，我遇到了一个问题，请重新提问。"
            })
```

```
层级图：

agent_loop（兜底，bot 永不崩）
  └── dispatch_tool（工具调用错误 → 告诉 AI 重试）
        └── execute_sql（网络超时 → 转成友好错误信息）
              └── requests.post（最底层，抛出原始异常）
```

**每一层只处理自己关心的错误，处理不了的往上抛。最外层兜底，保证 bot 永远不崩。**

---

## 和 retry [[decorator]] 配合

`@retry` 就是 exception handling 的一种封装：

```python
@retry(max_attempts=3)
def execute_sql(sql):
    response = requests.post(URL, json={"sql": sql}, timeout=10)
    return response.json()

# 等价于手写的 [[for-loop|for 循环]] + try/except：
def execute_sql(sql):
    for attempt in range(3):
        try:
            response = requests.post(URL, json={"sql": sql}, timeout=10)
            return response.json()      # 成功了 → return 退出整个函数
        except Exception:
            if attempt == 2:
                raise                   # 第 3 次还失败，往上抛
            # 否则继续下一轮循环
```

---

## 速查表

| 关键词 | 一句话 |
|--------|--------|
| `try` | 试试看，可能出错的代码放这里 |
| `except` | 如果出了某种错，走这里 |
| `finally` | 不管成败都执行（清理资源） |
| `raise` | 主动抛异常（拒绝危险操作） |
| 分层处理 | 每层处理自己关心的错误，处理不了的往上抛 |

---

## 相关笔记

- [[decorator]] — retry decorator 是异常处理的封装
- [[for-loop]] — for 循环基础 + retry 中的循环逻辑
- [[function]] — 函数基础
- [[dictionary]] — KeyError 来自字典找不到 key
- [[database/connection]] — 连接泄漏问题和 finally 的作用
- [[concurrency/threading]] — 线程中的异常处理
