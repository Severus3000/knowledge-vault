# Decorator（装饰器）

给函数"包一层"，不改原函数代码就能加功能。

---

## 前置知识：函数是"东西"

### 函数可以赋值给变量

在 Python 里，[[function|函数]]和数字、字符串一样，是一个"东西"（对象），可以赋值给变量：

```python
def say_hi():
    print("你好")

x = say_hi        # 没有括号！不是调用，是把函数本身赋值给 x
x()                # 调用 x，等于调用 say_hi，打印 "你好"
```

关键区别：

| 写法 | 含义 |
|------|------|
| `x = say_hi` | 把函数本身赋给 x，x 现在也是一个函数，`x()` 可以调用 |
| `x = say_hi()` | 先调用 say_hi，把返回值赋给 x（这里返回 None），`x()` 会报错 |

### 函数可以当参数传给另一个函数

```python
def call_twice(func):    # func 是一个参数，碰巧接收的是一个函数
    func()               # 第一次调用
    func()               # 第二次调用

call_twice(say_hi)    # 打印两次 "你好"
```

`call_twice(say_hi)` 传的是**函数本身**，不是 `say_hi()` 的返回值。
类比：`say_hi` = 把遥控器递过去让别人按；`say_hi()` = 自己按了按钮。

`call_twice` 之所以调用两次，纯粹因为我们写了两行 `func()`，没有什么特殊机制。

**如果函数不接受参数呢？** 比如 `say_hi()` 没有参数，你硬传一个函数给它：

```python
say_hi(some_function)
# TypeError: say_hi() takes 0 positional arguments but 1 was given
```

要想接收，就得在定义时加参数：`def say_hi(func):`。

### 函数里面可以定义函数

```python
def outer():
    def inner():
        print("我是内部函数")
    inner()

outer()     # 打印 "我是内部函数"
inner()     # ❌ 报错！inner 只在 outer 里面存在
```

### 函数可以返回函数

```python
def outer():
    def inner():
        print("我是内部函数")
    return inner        # 不调用 inner，把它当东西返回出去

result = outer()        # result 现在就是 inner 函数
result()                # 打印 "我是内部函数"
```

---

## Decorator 的本质

把上面几个特性组合起来：接收一个函数，返回一个"包装过的"新函数。

```python
def log(func):              # 接收一个函数作为参数
    def wrapper():          # 定义一个新函数（包装器）
        print("开始执行")    # 执行前做的事（装饰）
        func()              # 调用原函数（不变）
        print("执行完毕")    # 执行后做的事（装饰）
    return wrapper          # 返回这个新函数（不是调用结果！没有括号）
```

注意 `return wrapper` 不是 `return wrapper()`——返回的是**函数本身**，不是调用结果。这样调用者拿到的是一个新函数，可以之后再调用。

### 逐行执行 `new_func = log(say_hi)`

```
进入 log(func)，此时 func = say_hi

  定义了一个 wrapper 函数（还没执行，只是定义）
  wrapper 里面会：
    1. print("开始执行")
    2. 调用 func()，也就是 say_hi()
    3. print("执行完毕")

  return wrapper    → 把 wrapper 返回出去

出来了。new_func = wrapper
```

### 调用 `new_func()`

```
进入 wrapper()

  print("开始执行")     → 屏幕显示：开始执行
  func()               → 也就是 say_hi() → 屏幕显示：你好
  print("执行完毕")     → 屏幕显示：执行完毕
```

原来的 say_hi 没改一行代码，但现在执行前后多了日志。

---

## `@` 语法 = 自动替换

```python
# 这两种写法完全一样：

# 写法 A：手动替换
def say_hi():
    print("你好")
say_hi = log(say_hi)       # 用 wrapper 替换了 say_hi

# 写法 B：用 @ 语法糖
@log
def say_hi():
    print("你好")
# Python 看到 @ 会自动执行：say_hi = log(say_hi)
```

`@` 不是魔法，Python 看到它会自动把下面的函数传给 `log()`，然后用返回值替换原函数。

---

## 处理有参数的函数

上面的 `wrapper()` 没有参数，只能装饰无参函数。实际工具函数都有参数，所以用 [[function#*args 和 **kwargs|*args, **kwargs]]（"接受任意参数"）做透传：

```python
def log(func):
    def wrapper(*args, **kwargs):       # *args, **kwargs = 接收任意参数
        print(f"开始执行 {func.__name__}")
        result = func(*args, **kwargs)  # 把参数原封不动传给原函数
        print(f"执行完毕")
        return result                   # 把原函数的返回值也传回去
    return wrapper

@log
def execute_sql(sql):
    return f"查询结果：{sql}"
```

和最简版的两个区别：
1. **`wrapper(*args, **kwargs)`** — 不管原函数要什么参数，全部接住再透传给 `func()`
2. **`result = func(...)` + `return result`** — 保留原函数的返回值，调用者还能拿到结果

### 逐行走 `execute_sql("SELECT * FROM sales")`

```
execute_sql 已经被替换成 wrapper 了（因为 @log）

进入 wrapper(*args, **kwargs)
  此时 args = ("SELECT * FROM sales",)
  
  print(f"开始执行 {func.__name__}")
    → func.__name__ = "execute_sql"
    → 屏幕显示：开始执行 execute_sql

  result = func(*args, **kwargs)
    → func = 原来的 execute_sql
    → func("SELECT * FROM sales")
    → return "查询结果：SELECT * FROM sales"
    → result = "查询结果：SELECT * FROM sales"

  print("执行完毕")
    → 屏幕显示：执行完毕

  return result
    → 返回 "查询结果：SELECT * FROM sales"
```

---

## 带参数的 Decorator（三层嵌套）

有时候 decorator 自己也需要参数，比如 `@retry(max_attempts=3)`：

```python
def retry(max_attempts):            # 第一层：接收 decorator 的参数
    def decorator(func):            # 第二层：接收被装饰的函数
        def wrapper(*args, **kwargs):   # 第三层：实际执行的包装器
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise       # 把 except 捕获到的错误原样再抛出，程序报错
                    print(f"第 {attempt+1} 次失败，重试...")
        return wrapper
    return decorator
```

`raise` 单独写不带任何东西 = "把刚才 `except` 接住的那个错误原样扔出去"。
逻辑：前几次失败我给你重试机会，最后一次还不行就不管了，报错。

```python
@retry(max_attempts=3)
def execute_sql(sql):
    return requests.post(URL, json={"sql": sql})
```

### 拆解 `@retry(max_attempts=3)` 的执行过程

```
Python 看到 @retry(max_attempts=3)，分两步执行：

第 1 步：调用 retry(max_attempts=3)
  进入 retry，max_attempts = 3
  定义 decorator 函数
  return decorator
  → 得到 decorator

第 2 步：调用 decorator(execute_sql)    ← 跟普通的 @log 一样了
  进入 decorator，func = execute_sql
  定义 wrapper 函数
  return wrapper
  → execute_sql 被替换成 wrapper
```

等价于：
```python
execute_sql = retry(max_attempts=3)(execute_sql)
#            ↑ 返回 decorator      ↑ decorator(execute_sql) 返回 wrapper
```

### 调用 `execute_sql("SELECT ...")` 时

```
进入 wrapper("SELECT ...")

  attempt = 0:
    try: func("SELECT ...") → 假设网络超时，抛出异常
    except: "第 1 次失败，重试..."

  attempt = 1:
    try: func("SELECT ...") → 假设又超时
    except: "第 2 次失败，重试..."

  attempt = 2:
    try: func("SELECT ...") → 成功了！return 结果
    （如果还失败，raise 抛出异常，不再重试）
```

---

## Agent 场景：工具自动注册

用 decorator + [[dictionary]] 配合，实现工具自动注册。

```python
TOOL_REGISTRY = {}          # 空的 [[dictionary|dict]]

def tool(name):             # 第一层：接收工具名
    def decorator(func):    # 第二层：接收函数
        TOOL_REGISTRY[name] = func    # 注册！把函数存进 dict
        return func         # 原封不动返回原函数（不需要包装）
    return decorator

@tool("execute_sql")
def execute_sql(sql: str):
    return db.query(sql)

@tool("search_knowledge")
def search_knowledge(query: str):
    return kb.search(query)
```

### 逐行走一遍

```
Python 读到 @tool("execute_sql")：

第 1 步：调用 tool("execute_sql")
  进入 tool，name = "execute_sql"
  定义 decorator
  return decorator

第 2 步：调用 decorator(execute_sql)
  进入 decorator，func = execute_sql
  TOOL_REGISTRY["execute_sql"] = execute_sql    ← 注册进 [[dictionary|dict]] 了！
  return func    ← 不包装，原函数不变

Python 读到 @tool("search_knowledge")：
  同样的流程
  TOOL_REGISTRY["search_knowledge"] = search_knowledge

最终 TOOL_REGISTRY = {
    "execute_sql": <execute_sql 函数>,
    "search_knowledge": <search_knowledge 函数>,
}
```

以后 AI 返回 `tool_call: execute_sql`，dispatch 就一行（用字符串从 [[dictionary|dict]] 取出函数再调用）：
```python
tool_name = "execute_sql"                       # LLM 返回的字符串
result = TOOL_REGISTRY[tool_name](**tool_args)   # 字典查找 → 拿到函数 → 调用
```

不用手动维护 dict，加新工具只要写 `@tool("名字")` 就自动注册了。

LangChain、OpenAI function calling 框架全都是这个模式。

---

## 叠加多个 Decorator

```python
@retry(max_attempts=3)       # 外层：失败了重试
@log                         # 内层：打日志
@tool("execute_sql")         # 最内层：注册到工具表
def execute_sql(sql: str):
    return requests.post(URL, json={"sql": sql})
```

执行顺序从外到内包裹，调用时从外到内执行：
```
retry 检查要不要重试
  → log 打日志
    → tool 已经注册过了，直接调原函数
      → execute_sql 真正执行
```

---

## 速查表

| 概念 | 一句话 |
|------|--------|
| Decorator | 给函数包一层，不改原函数就能加功能 |
| `@` 语法 | `@log` 等于 `func = log(func)`，语法糖 |
| 两层嵌套 | `log(func)` → 无参 decorator |
| 三层嵌套 | `retry(n)(func)` → 带参 decorator |
| 工具注册 | `@tool("name")` 自动把函数收集到 registry |
| 叠加 | 多个 `@` 从外到内包裹，像套娃 |

---

## 相关笔记

- [[function]] — 函数基础（一等公民、参数、返回值）
- [[dictionary]] — 字典基础 + 工具注册表模式详解
- [[generator-yield]] — generator（另一个 agent 开发常用概念）
