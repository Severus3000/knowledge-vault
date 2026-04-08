# Python for Agent Development — Learning Plan

针对 agent 开发需要的 Python 知识点，按优先级排列。

---

## 已完成

| # | 主题 | 笔记 | 核心收获 |
|---|------|------|---------|
| 1 | 并发总览 | `concurrency/concurrency-overview.md` | 线程/进程/异步三种方式对比 |
| 2 | 线程 | `concurrency/threading.md` | start、join、daemon |
| 3 | 线程安全 | `concurrency/thread-safety.md` | race condition、lock、drain |
| 4 | 进程 | `concurrency/process.md` | IPC、subprocess、parallel agent |
| 5 | 异步 | `concurrency/async-await.md` | await、event loop |
| 6 | Generator | `generator-yield.md` | yield、流式输出 |
| 7 | Decorator | `decorator.md` | @语法、工具注册、retry |
| 8 | Exception Handling | `exception-handling.md` | try/except、分层错误处理 |

---

## 待学习

### 9. Closure（闭包）与高阶函数

**为什么重要**：s02 的 tool dispatch map 里的 lambda、decorator 的底层原理都依赖闭包。

**要讲的内容**：
- 什么是闭包：内部函数"记住"了外部函数的变量
- 为什么 decorator 的 wrapper 能访问 func — 因为闭包
- 高阶函数：接收函数或返回函数的函数（map、filter、sorted 的 key 参数）
- Agent 场景：tool dispatch 里的 lambda，回调函数

**前置知识**：decorator（已学）

---

### 10. Pydantic / dataclass（结构化数据）

**为什么重要**：工具参数校验、LLM 结构化输出、API 请求/响应的数据建模。

**要讲的内容**：
- dataclass：Python 内置，快速定义数据结构
- Pydantic：dataclass 的增强版，自带类型校验
- Agent 场景：定义 tool schema（参数类型、必填/可选、描述）
- Agent 场景：强制 LLM 输出结构化 JSON（structured output）
- 实际框架怎么用：LangChain 的 `@tool` 自动从 Pydantic model 生成 JSON schema

**前置知识**：type hints（会一起讲基础）

---

### 11. Dict / List Comprehension（推导式）

**为什么重要**：agent 里大量的数据转换——过滤消息、提取 tool_calls、构造 messages 列表。

**要讲的内容**：
- List comprehension：`[x for x in list if condition]`
- Dict comprehension：`{k: v for k, v in items}`
- Agent 场景：从 messages 里过滤出所有 tool_result
- Agent 场景：把 tool schema 列表转成 dispatch dict
- 和 for 循环的对比：什么时候用推导式，什么时候用普通 for

**前置知识**：无

---

### 12. Type Hints（类型注解）

**为什么重要**：工具函数的参数类型、IDE 自动补全、Pydantic 的基础。

**要讲的内容**：
- 基础语法：`def func(name: str, age: int) -> bool:`
- 常用类型：`Optional`、`Union`、`list[str]`、`dict[str, Any]`
- Agent 场景：工具函数签名 → 自动生成 tool schema 给 LLM
- 运行时不强制：type hints 只是"标签"，Python 不会自动检查

**前置知识**：无

---

## 建议学习顺序

```
已完成                              待学习
并发 → Generator → Decorator → Exception Handling
                       ↓
                    Closure（decorator 的底层原理）
                       ↓
                    Type Hints（Pydantic 的前置）
                       ↓
                    Pydantic / dataclass
                       ↓
                    Dict/List Comprehension
```

---

## 目录结构

```
python/
├── LEARNING-PLAN.md              ← 本文件
├── generator-yield.md            ✅
├── decorator.md                  ✅
├── exception-handling.md         ✅
├── closure.md                    ⬜ 待创建
├── type-hints.md                 ⬜ 待创建
├── pydantic-dataclass.md         ⬜ 待创建
├── comprehension.md              ⬜ 待创建
└── concurrency/
    ├── concurrency-overview.md   ✅
    ├── threading.md              ✅
    ├── thread-safety.md          ✅
    ├── process.md                ✅
    └── async-await.md            ✅
```
