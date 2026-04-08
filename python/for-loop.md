# For Loop（for 循环）

把一组东西逐个拿出来处理。

---

## 基础

```python
for x in [1, 2, 3]:
    print(x)

# 输出：
# 1
# 2
# 3
```

每轮循环把列表里的下一个值赋给 `x`，然后执行循环体。

---

## range() — 循环 N 次

`range(n)` 生成 `0` 到 `n-1` 的序列：

```python
range(3)    # → 0, 1, 2
range(5)    # → 0, 1, 2, 3, 4
```

```python
for i in range(3):
    print(i)

# 输出：
# 0
# 1
# 2
```

| 写法 | 生成 | 常用场景 |
|------|------|---------|
| `range(3)` | 0, 1, 2 | 循环 3 次 |
| `range(1, 4)` | 1, 2, 3 | 从 1 开始 |
| `range(0, 10, 2)` | 0, 2, 4, 6, 8 | 步长为 2 |

---

## 遍历不同类型

```python
# 列表
for name in ["张三", "李四", "王五"]:
    print(name)

# 字符串（逐个字符）
for char in "hello":
    print(char)        # h, e, l, l, o

# [[dictionary|字典]]
scores = {"数学": 90, "语文": 85}
for subject, score in scores.items():
    print(f"{subject}: {score}")
```

---

## break 和 continue

```python
# break — 立刻退出整个循环
for i in range(10):
    if i == 5:
        break          # 到 5 就不循环了
    print(i)           # 打印 0, 1, 2, 3, 4

# continue — 跳过这一轮，进入下一轮
for i in range(5):
    if i == 2:
        continue       # 跳过 2
    print(i)           # 打印 0, 1, 3, 4
```

---

## return 会退出整个函数（不只是循环）

```python
def find_first_even(numbers):
    for n in numbers:
        if n % 2 == 0:
            return n       # 找到第一个偶数就退出整个函数
    return None            # 都没找到

find_first_even([1, 3, 4, 6])   # 返回 4，不会继续看 6
```

这一点在 retry 场景里很关键——成功了就 return，循环自动结束。

---

## Agent 场景：retry 循环

`for` + `try/except` 实现重试逻辑（等价于 [[decorator#带参数的 Decorator（三层嵌套）|@retry decorator]]）：

```python
def execute_sql(sql):
    for attempt in range(3):       # 给 3 次机会：attempt = 0, 1, 2
        try:
            response = requests.post(URL, json={"sql": sql}, timeout=10)
            return response.json()   # ✅ 成功 → return 退出整个函数
        except Exception:
            if attempt == 2:         # 最后一次（0, 1, 2 中的 2）
                raise                # 报错，不再重试
            # 否则：什么都不做，for 循环自动进入下一轮
```

逐轮走一遍：

```
attempt = 0（第 1 次尝试）
  try: 发请求 → 💥 超时
  except: attempt 是 0，不等于 2 → 继续循环

attempt = 1（第 2 次尝试）
  try: 发请求 → 💥 又超时
  except: attempt 是 1，不等于 2 → 继续循环

attempt = 2（第 3 次尝试）
  try: 发请求 → 💥 还是超时
  except: attempt == 2 → raise，报错，不再重试
```

如果第 2 次就成功了：

```
attempt = 0 → 💥 超时 → 继续
attempt = 1 → ✅ 成功 → return response.json() → 退出整个函数
attempt = 2 → 不会执行（已经 return 了）
```

核心：`for` 给你 N 次机会，`return` 成功就走人，`raise` 用完机会就报错。

---

## 为什么 `attempt == 2` 而不是 `== 3`

`range(3)` 生成的是 `0, 1, 2`，最后一个是 **2**（不是 3）。

所以判断"是不是最后一次"：
- `range(3)` → 最后一次是 `attempt == 2`
- `range(max_attempts)` → 最后一次是 `attempt == max_attempts - 1`

---

## 相关笔记

- [[exception-handling]] — try/except 基础 + retry 场景
- [[decorator]] — @retry decorator（把 for + try/except 封装成 decorator）
- [[generator-yield]] — for 循环遍历 generator
- [[dictionary]] — for 循环遍历字典
