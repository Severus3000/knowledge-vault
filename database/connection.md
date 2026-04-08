# 数据库连接（Connection）

数据库连接是一种**有限资源**，用完必须关掉，不然会泄漏。

---

## 连接是什么

`db.connect()` 做的事：

1. 你的程序和数据库服务器之间建立一条网络通道（TCP 连接）
2. 认证（用户名密码）
3. 分配内存、创建会话

这条通道就是一个"连接"。它会一直占着资源，直到你 `conn.close()`。

---

## 为什么会"越积越多"

数据库有连接上限（比如 MySQL 默认 151 条）。每次 `connect()` 占一条：

```
请求 1 → connect() → 占 1 条     剩 150
请求 2 → connect() → 占 1 条     剩 149
请求 3 → connect() → 占 1 条     剩 148
...
```

**正常情况：** 用完 close，连接释放，别人可以用。

**泄漏情况：** connect 了但没 close（比如中途出错跳过了 close），这条连接就一直占着，没人能用它，也没人会释放它。

```python
# 泄漏：出错时 close 不会执行
def query(sql):
    conn = db.connect()            # 占了一条
    result = conn.execute(sql)     # 💥 出错！跳到异常
    conn.close()                   # 跳过了！连接没关
    return result
```

调 100 次崩 100 次 → 泄漏 100 条连接 → 第 101 个请求连不上 → 整个服务挂掉。

---

## 解决：finally 保证关闭

```python
def query(sql):
    conn = db.connect()
    try:
        result = conn.execute(sql)
        return result
    except Exception as e:
        print(f"查询失败：{e}")
        return None
    finally:
        conn.close()       # 不管成功还是失败，一定执行
```

更常用的写法是 `with` 语句（Python 自动帮你关）：

```python
with db.connect() as conn:         # 进入时 connect
    result = conn.execute(sql)     # 正常使用
# 离开 with 块时自动 close，不管有没有出错
```

`with` 底层就是帮你写了 try/finally。

---

## 连接池（Connection Pool）

每次 connect/close 开销很大（网络握手、认证）。实际项目用**连接池**——提前建好一批连接，用的时候借一个，用完还回去：

```
连接池（10 条连接待命）
  请求 A 来了 → 借一条 → 用完还回去
  请求 B 来了 → 借一条 → 用完还回去
  10 条都在用 → 请求 C 排队等
```

不用每次都建新连接，快很多。也不怕忘了 close——池子会自动回收。

---

## 你的 bot 不用管这些

你的 bot 不直接连数据库——它调 Node.js 云函数（HTTP 请求），云函数内部管理连接。

```
Python bot → HTTP 请求 → Node.js 云函数 → 数据库
                          ↑ 这里管连接，不是你的事
```

但理解连接泄漏的概念很重要，因为 HTTP 请求也是资源，原理一样——发出去的请求要处理完，超时要 close，不然也会积压。

---

## 相关笔记

- [[python/function]] — finally 和 try/except 的用法
- [[python/decorator]] — retry decorator 用 try/except 实现重试
