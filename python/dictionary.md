# Dictionary（字典）

字典是 key-value 对的集合。用 key 查 value，速度极快（O(1)）。

---

## 基础操作

```python
# 创建
d = {}                          # 空字典
d = {"name": "Rui", "age": 30} # 带初始值

# 读
d["name"]                       # "Rui"
d.get("name")                   # "Rui"（key 不存在时返回 None，不报错）
d.get("phone", "未知")          # key 不存在时返回默认值 "未知"

# 写
d["email"] = "rui@example.com"  # 新增
d["age"] = 31                   # 修改（key 已存在就覆盖）

# 删
del d["age"]                    # 删除
d.pop("age", None)              # 删除，key 不存在也不报错

# 检查 key 是否存在
"name" in d                     # True
"phone" in d                    # False
```

---

## 遍历

```python
d = {"name": "Rui", "age": 30, "city": "Shanghai"}

# 遍历 key
for k in d:
    print(k)                # name, age, city

# 遍历 value
for v in d.values():
    print(v)                # Rui, 30, Shanghai

# 遍历 key + value
for k, v in d.items():
    print(f"{k}: {v}")      # name: Rui, age: 30, city: Shanghai
```

---

## Value 可以是任何类型

字符串、数字、列表、甚至函数：

```python
d = {
    "name": "Rui",                  # 字符串
    "scores": [90, 85, 95],         # 列表
    "greet": lambda: print("hi"),   # 函数
}

d["greet"]()    # 打印 "hi"
```

---

## Agent 场景：用字典做工具注册表

这是 decorator + dictionary 配合的典型用法。

### 问题

LLM 返回的是字符串（工具名），你需要把字符串变成实际的函数调用。

### 方案：字典当桥梁

```python
TOOL_REGISTRY = {}

def register(func):
    TOOL_REGISTRY[func.__name__] = func   # func.__name__ 是函数名字符串
    return func

@register
def execute_sql(sql):
    return f"查询结果：{sql}"

@register
def search_knowledge(query):
    return f"搜索结果：{query}"
```

注册后字典长这样：

```python
{
    "execute_sql": <function execute_sql>,
    "search_knowledge": <function search_knowledge>,
}
```

Agent 调用工具的流程：

```python
# LLM 说要用 "execute_sql"，参数是 "SELECT * FROM sales"
tool_name = "execute_sql"
tool_args = {"sql": "SELECT * FROM sales"}

fn = TOOL_REGISTRY[tool_name]       # 用字符串从字典取出函数
result = fn(**tool_args)             # 调用，** 把 dict 展开成关键字参数
# result = "查询结果：SELECT * FROM sales"
```

```
LLM 返回 tool_name（字符串）
        ↓
TOOL_REGISTRY[tool_name] → 拿到函数
        ↓
fn(**tool_args) → 调用函数，拿到结果
        ↓
把结果返回给 LLM
```

### 为什么不用 if/elif

```python
# 不好：每加一个工具要改这里
if tool_name == "execute_sql":
    result = execute_sql(sql)
elif tool_name == "search_knowledge":
    result = search_knowledge(query)
elif ...

# 好：加工具只需要 @register，这里不用改
fn = TOOL_REGISTRY[tool_name]
result = fn(**tool_args)
```

---

## 相关笔记

- [[function]] — 函数作为一等公民，decorator 注册模式
- [[generator-yield]] — generator 也常和字典配合使用
