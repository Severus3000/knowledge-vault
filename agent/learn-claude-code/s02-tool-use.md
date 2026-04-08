# s02 - Tool Use（工具使用）

`s01 > [ s02 ] s03 > s04 > s05 > s06 | s07 > s08 > s09 > s10 > s11 > s12`

> **核心格言**：*"加一个工具，只加一个 handler"* -- 循环不用动，新工具注册进 dispatch map 就行。

---

## 问题

s01 只有一个 `bash` 工具。乍一看够用了 -- bash 什么都能干嘛。但实际用起来有两个大问题：

**1. 不安全** -- bash 能干任何事。`rm -rf /`、`curl` 下载恶意脚本、读 `/etc/passwd` -- 黑名单永远堵不完。每次 bash 调用都是一个**不受约束的安全面**。

**2. 不精确** -- 让 AI 用 bash 操作文件时：
- `cat` 输出截断不可预测
- `sed` 遇到特殊字符（引号、反斜杠、正则元字符）就崩
- 写文件要用 heredoc 或 echo 拼接，极易出错
- AI 生成的 bash 命令越长，出错概率越高

**本质问题**：bash 是"瑞士军刀" -- 什么都能做，但什么都做不好。

---

## 解决方案：Dispatch Map（分发表）

```
+--------+      +-------+      +------------------+
|  User  | ---> |  LLM  | ---> | Tool Dispatch    |
| prompt |      |       |      | {                |
+--------+      +---+---+      |   bash: run_bash |
                    ^           |   read: run_read |
                    |           |   write: run_wr  |
                    +-----------+   edit: run_edit |
                    tool_result | }                |
                                +------------------+
```

一个字典，把工具名映射到处理函数。AI 说"我要用 read_file"，代码查字典找到对应的函数来执行。

---

## s01 硬编码 vs s02 字典查找

**s01 的做法** -- 硬编码，只认识 bash：

```python
for block in response.content:
    if block.type == "tool_use":
        output = run_bash(block.input["command"])  # hardcoded to bash
```

如果要加第二个工具，你就得写 `if/elif`：

```python
if block.name == "bash":
    output = run_bash(block.input["command"])
elif block.name == "read_file":
    output = run_read(block.input["path"])
elif block.name == "write_file":
    ...
```

工具越多，这串 `if/elif` 越长，越难维护。

**s02 的做法** -- 字典查找，一行搞定：

```python
handler = TOOL_HANDLERS.get(block.name)
output = handler(**block.input) if handler else f"Unknown tool: {block.name}"
```

不管有 4 个工具还是 40 个工具，这两行代码永远不变。

---

## TOOL_HANDLERS 字典

```python
TOOL_HANDLERS = {
    "bash":       lambda **kw: run_bash(kw["command"]),
    "read_file":  lambda **kw: run_read(kw["path"], kw.get("limit")),
    "write_file": lambda **kw: run_write(kw["path"], kw["content"]),
    "edit_file":  lambda **kw: run_edit(kw["path"], kw["old_text"], kw["new_text"]),
}
```

四个工具，四行代码。每个 lambda 负责从 AI 传来的参数字典中提取正确的参数，调用对应的处理函数。

加新工具 = **写一个处理函数 + 字典加一行**。循环不改。

---

## 四个工具各司其职

| 工具 | 功能 | 替代了什么 bash 操作 |
|------|------|---------------------|
| `bash` | 跑 shell 命令 | 保留，用于非文件操作 |
| `read_file` | 读文件内容 | `cat`（但可控截断，不会爆掉） |
| `write_file` | 写文件 | `echo > file`、heredoc（但不怕特殊字符） |
| `edit_file` | 精确替换文件中的文本 | `sed`（但不怕正则元字符） |

每个专用工具都比用 bash 更安全、更精确。

---

## 路径沙箱 safe_path()

```python
WORKDIR = Path.cwd()

def safe_path(p: str) -> Path:
    path = (WORKDIR / p).resolve()
    if not path.is_relative_to(WORKDIR):
        raise ValueError(f"Path escapes workspace: {p}")
    return path
```

这个函数做一件事：确保 AI 传来的路径不会逃出工作目录。

- `(WORKDIR / p).resolve()` -- 拼接路径并解析掉 `..`
- `is_relative_to(WORKDIR)` -- 检查解析后的路径是否还在工作目录内
- 如果 AI 试图 `read_file("../../etc/passwd")`，`resolve()` 会解析成 `/etc/passwd`，然后 `is_relative_to` 检查失败，抛异常

所有文件操作工具（read/write/edit）都经过 `safe_path()`。bash 工具仍然不受限 -- 这是有意为之，保留它作为"万能后备"。

---

## 循环几乎没变

对比 s01 和 s02 的循环核心：

```python
# s01: hardcoded
for block in response.content:
    if block.type == "tool_use":
        output = run_bash(block.input["command"])

# s02: dispatch map
for block in response.content:
    if block.type == "tool_use":
        handler = TOOL_HANDLERS.get(block.name)
        output = handler(**block.input) if handler else f"Unknown tool: {block.name}"
```

只改了**一行**。循环结构、消息追加、stop_reason 检查 -- 全都不变。

---

## 类比

| | s01 | s02 |
|---|---|---|
| 比喻 | **瑞士军刀** -- bash 什么都干 | **工具箱** -- 各司其职 |
| 安全 | 黑名单（堵不完） | 沙箱（白名单式路径限制） |
| 精确度 | 依赖 AI 生成正确的 bash | 专用函数，参数明确 |
| 扩展性 | 加工具要改循环 | 加工具只改字典 |

---

## 跟 mattress bot 的关系

我们的床垫业务 bot 用的是完全相同的 dispatch map 模式，只是工具不同：

```python
# 床垫 bot 的 dispatch map（概念上）
TOOL_HANDLERS = {
    "execute_sql":        lambda **kw: call_backend("bot-execute-sql", kw),
    "search_knowledge":   lambda **kw: call_backend("bot-search-knowledge", kw),
    "get_smartsheet_link": lambda **kw: call_backend("bot-smartsheet-link", kw),
}
```

工具从"读写文件"变成了"查数据库、搜知识、拿报表链接" -- 但**分发机制完全一样**。这就是 dispatch map 的价值：循环和工具是解耦的，循环不关心你有几个工具，也不关心工具干什么。

---

## 变更总结

| 组件 | 之前（s01） | 之后（s02） |
|------|------------|------------|
| Tools | 1（仅 bash） | 4（bash, read, write, edit） |
| Dispatch | 硬编码 bash 调用 | `TOOL_HANDLERS` 字典 |
| 路径安全 | 无 | `safe_path()` 沙箱 |
| Agent loop | 不变 | 不变 |

**总结：循环和工具是解耦的。循环不关心有几个工具，也不关心工具干什么。加工具只需要写一个函数、字典加一行。**
