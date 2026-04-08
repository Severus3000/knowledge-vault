# Function（函数）

函数是 Python 里最基本的代码组织单位。定义一段逻辑，给它起个名字，之后随时调用。

---

## 基础：定义和调用

```python
def say_hi():
    print("你好")

say_hi()    # 调用，打印 "你好"
```

- `def` 定义函数
- `say_hi()` 带括号 = 调用
- `say_hi` 不带括号 = 函数本身（一个对象）

---

## 参数和返回值

```python
def add(a, b):
    return a + b

result = add(3, 5)    # result = 8
```

没有 `return` 的函数返回 `None`：

```python
def greet(name):
    print(f"你好 {name}")

x = greet("Rui")    # 打印 "你好 Rui"
print(x)             # None
```

---

## *args 和 **kwargs

`*args` 收集所有**位置参数**，变成 tuple：

```python
def foo(*args):
    print(args)

foo(1, 2, 3)       # args = (1, 2, 3)
foo("hello")        # args = ("hello",)
```

`**kwargs` 收集所有**关键字参数**，变成 dict：

```python
def foo(**kwargs):
    print(kwargs)

foo(name="Rui", age=30)   # kwargs = {"name": "Rui", "age": 30}
```

两个一起用 = "接受任意参数"：

```python
def foo(*args, **kwargs):
    print(args, kwargs)

foo(1, 2, name="Rui")   # args = (1, 2)   kwargs = {"name": "Rui"}
```

---

## 函数是"一等公民"

Python 里函数和数字、字符串一样，是一个对象，可以：

### 1. 赋值给变量

```python
def say_hi():
    print("你好")

x = say_hi     # 没有括号！把函数本身赋给 x
x()             # 调用 x，等于调用 say_hi，打印 "你好"
```

关键区别：

| 写法 | 含义 |
|------|------|
| `x = say_hi` | 把函数本身赋给 x，x 现在是一个函数 |
| `x = say_hi()` | 调用 say_hi，把返回值赋给 x（这里是 None） |

### 2. 当参数传给另一个函数

```python
def call_twice(func):    # func 是一个参数，碰巧它是个函数
    func()               # 第一次调用
    func()               # 第二次调用

call_twice(say_hi)       # 打印两次 "你好"
```

`call_twice(say_hi)` 传的是函数本身，不是 `say_hi()` 的返回值。

类比：`say_hi` = 把遥控器递过去，`say_hi()` = 你自己按了按钮。

### 3. 从函数里返回

```python
def make_greeter(name):
    def greet():
        print(f"你好 {name}")
    return greet            # 返回一个函数

hi_rui = make_greeter("Rui")
hi_rui()                    # 打印 "你好 Rui"
```

---

## Decorator（装饰器）

函数能传来传去，就有了 decorator——在不改原函数代码的前提下，给它加功能。

### 最简版

```python
def decorator(func):
    def wrapper():
        print("before")
        func()              # 调用原函数
        print("after")
    return wrapper          # 返回新函数（不是调用结果！）

@decorator
def say_hi():
    print("你好")

# @decorator 等价于：say_hi = decorator(say_hi)
# 现在 say_hi 指向 wrapper
```

调用 `say_hi()` 输出：

```
before
你好
after
```

原函数代码没变，但行为被"装饰"了。

### 通用版：处理参数和返回值

```python
def log(func):
    def wrapper(*args, **kwargs):         # 接收任意参数
        print(f"开始执行 {func.__name__}")
        result = func(*args, **kwargs)    # 原样转发参数，接住返回值
        print("执行完毕")
        return result                     # 把返回值传回去
    return wrapper

@log
def execute_sql(sql):
    return f"查询结果：{sql}"

answer = execute_sql("SELECT * FROM sales")
# 打印：开始执行 execute_sql
# 打印：执行完毕
# answer = "查询结果：SELECT * FROM sales"
```

和最简版的区别：
1. `wrapper(*args, **kwargs)` — 不管原函数要什么参数，全部接住再透传
2. `result = func(...)` + `return result` — 保留原函数的返回值

### 注册型 decorator（不包装）

不是所有 decorator 都要加 wrapper。可以只用来"登记"：

```python
TOOL_REGISTRY = {}

def register(func):
    TOOL_REGISTRY[func.__name__] = func   # 存进字典
    return func                            # 原样返回，不包装

@register
def execute_sql(sql):
    return f"查询结果：{sql}"

@register
def search_knowledge(query):
    return f"搜索结果：{query}"
```

现在 `TOOL_REGISTRY` 是：

```python
{
    "execute_sql": <function execute_sql>,
    "search_knowledge": <function search_knowledge>,
}
```

函数没被改变，只是被收集到字典里了。Agent 可以用字符串名字查找并调用：

```python
tool_name = "execute_sql"                       # LLM 返回的字符串
fn = TOOL_REGISTRY[tool_name]                   # 从字典取出函数
result = fn("SELECT * FROM sales")              # 调用
```

### 带参数的 decorator（三层嵌套）

decorator 自己也需要参数时，多套一层：

```python
def retry(max_attempts):              # 第一层：接收 decorator 的参数
    def decorator(func):              # 第二层：接收被装饰的函数
        def wrapper(*args, **kwargs): # 第三层：实际执行的包装器
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise          # 最后一次还失败，把错误抛出去
                    print(f"第 {attempt+1} 次失败，重试...")
        return wrapper
    return decorator

@retry(max_attempts=3)
def execute_sql(sql):
    return call_backend(sql)
```

`raise` 单独写 = 把 `except` 捕获到的错误原样再抛出。意思是"重试机会用完了，报错吧"。详见 [[exception-handling#raise — 主动抛异常]]。

---

## 相关笔记

- [[dictionary]] — 字典，decorator 注册模式的核心数据结构
- [[exception-handling]] — try/except/finally/raise
- [[for-loop]] — for 循环，retry decorator 里的核心
- [[generator-yield]] — generator 也是特殊的函数
- [[concurrency/async-await]] — async 函数
