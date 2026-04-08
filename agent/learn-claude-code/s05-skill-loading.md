# s05 - Skill Loading（按需知识加载）

`s01 > s02 > s03 > s04 > [ s05 ] s06 | s07 > s08 > s09 > s10 > s11 > s12`

> **核心格言**：*"用到什么知识，临时加载什么知识"* -- 目录便宜放 system prompt，正文贵按需加载。

---

## 问题

AI agent 需要领域知识才能做专业的事。代码审查需要审查清单，数据库查询需要表结构，业务分析需要产品目录。

最直觉的做法：把所有知识塞进 system prompt。问题是：

- 10 个 skill，每个 2000 token = **20000 token**，还没开始干活就用掉了
- 大部分对话只用到 1-2 个 skill，其他 8 个白白占位
- token 是要花钱的，更关键的是**占用了上下文窗口的注意力**

类比：你去餐厅，服务员把所有菜的**完整做法**念一遍（20 分钟），还是给你一本**菜单目录**（10 秒看完），你点了再去后厨拿详细做法？

---

## 解决方案：两层设计

```
System prompt:                           tool_result:
+--------------------------------------+ +--------------------------------------+
| You are a coding agent.              | | <skill name="code-review">           |
| Skills available:                    | |   Full code review instructions      |
|   - pdf: Process PDF files...        | |   Step 1: ...                        |
|   - code-review: Review code...      | |   Step 2: ...                        |
+--------------------------------------+ | </skill>                             |
                                         +--------------------------------------+
 Layer 1: 目录（~100 token/skill）         Layer 2: 正文（~2000 token/skill）
 便宜，始终在场                              贵，按需加载
```

| 层 | 放在哪里 | 内容 | 成本 |
|---|---------|------|------|
| **Layer 1** | system prompt | skill 名称 + 一句话简介 | ~100 token/skill，始终消耗 |
| **Layer 2** | tool_result（AI 调用 `load_skill` 后） | 完整知识正文 | ~2000 token/skill，仅按需消耗 |

AI 看到目录就知道有哪些知识可用，需要时调用 `load_skill("code-review")`，完整内容通过 tool_result 注入上下文。

---

## Skill 存储格式

每个 skill 是一个目录，里面有一个 `SKILL.md` 文件：

```
skills/
  pdf/
    SKILL.md
  code-review/
    SKILL.md
  mattress-bot/
    SKILL.md
```

`SKILL.md` 格式 -- YAML frontmatter + 正文：

```markdown
---
name: code-review
description: Code review checklist and standards
tags: development
---

## Code Review Checklist

1. Check for security vulnerabilities
2. Verify error handling
3. Review naming conventions
...
```

frontmatter 提供 Layer 1 需要的元数据（名称、简介、标签），正文是 Layer 2 的完整知识。

---

## SkillLoader 类

```python
class SkillLoader:
    def __init__(self, skills_dir: Path):
        self.skills_dir = skills_dir
        self.skills = {}
        self._load_all()

    def _load_all(self):
        if not self.skills_dir.exists():
            return
        for f in sorted(self.skills_dir.rglob("SKILL.md")):
            text = f.read_text()
            meta, body = self._parse_frontmatter(text)
            name = meta.get("name", f.parent.name)
            self.skills[name] = {"meta": meta, "body": body, "path": str(f)}

    def _parse_frontmatter(self, text: str) -> tuple:
        match = re.match(r"^---\n(.*?)\n---\n(.*)", text, re.DOTALL)
        if not match:
            return {}, text
        try:
            meta = yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError:
            meta = {}
        return meta, match.group(2).strip()
```

初始化时扫描 `skills/` 目录下所有 `SKILL.md`，解析 frontmatter 和正文，存进字典。

两个关键方法：

### `get_descriptions()` -- 生成目录（Layer 1）

```python
def get_descriptions(self) -> str:
    lines = []
    for name, skill in self.skills.items():
        desc = skill["meta"].get("description", "No description")
        tags = skill["meta"].get("tags", "")
        line = f"  - {name}: {desc}"
        if tags:
            line += f" [{tags}]"
        lines.append(line)
    return "\n".join(lines)
```

输出类似：
```
  - pdf: Process PDF files [utility]
  - code-review: Code review checklist and standards [development]
  - mattress-bot: 床垫业务知识库 [business]
```

这段文字被直接嵌入 system prompt。

### `get_content()` -- 返回完整内容（Layer 2）

```python
def get_content(self, name: str) -> str:
    skill = self.skills.get(name)
    if not skill:
        return f"Error: Unknown skill '{name}'. Available: {', '.join(self.skills.keys())}"
    return f"<skill name=\"{name}\">\n{skill['body']}\n</skill>"
```

返回 `<skill>` 标签包裹的完整正文。这段内容通过 tool_result 进入 AI 的上下文。

---

## System Prompt 集成

```python
SKILL_LOADER = SkillLoader(SKILLS_DIR)

SYSTEM = f"""You are a coding agent at {WORKDIR}.
Use load_skill to access specialized knowledge before tackling unfamiliar topics.

Skills available:
{SKILL_LOADER.get_descriptions()}"""
```

system prompt 里只有目录，不到 100 token。告诉 AI "有这些知识可用，需要时调用 `load_skill`"。

---

## Dispatch Map 加一行

```python
TOOL_HANDLERS = {
    "bash":       lambda **kw: run_bash(kw["command"]),
    "read_file":  lambda **kw: run_read(kw["path"], kw.get("limit")),
    "write_file": lambda **kw: run_write(kw["path"], kw["content"]),
    "edit_file":  lambda **kw: run_edit(kw["path"], kw["old_text"], kw["new_text"]),
    "load_skill": lambda **kw: SKILL_LOADER.get_content(kw["name"]),  # 新增
}
```

s02 讲的 dispatch map 的价值在这里体现 -- 加一个新工具，只需要字典加一行。循环不改。

---

## 实际流程举例

用户问："帮我审查一下 main.py 的代码"

```
Round 1:
  AI 看到 system prompt 里的目录：
    "Skills available:
      - code-review: Code review checklist and standards"
  AI 决定先加载知识 → 调用 load_skill("code-review")
  tool_result 返回完整审查清单（~2000 token）

Round 2:
  AI 现在有了审查清单 + 代码文件
  → 调用 read_file("main.py")
  tool_result 返回文件内容

Round 3:
  AI 按照清单逐项审查代码
  → 生成审查报告（stop_reason = "end_turn"）
```

如果用户下一个问题是"帮我处理 PDF"，AI 会加载 `pdf` skill -- 按需加载，而不是一开始就把所有知识都塞进来。

---

## 跟 mattress bot 的关系

这是我们 bot 最关键的 session 之一。`skills/mattress-bot/SKILL.md` 会存放：

- **表结构**：哪些表、哪些字段、字段含义
- **产品知识**：床垫型号、材质、价格区间
- **促销方案**：历史促销活动、效果数据
- **业务规则**：折扣权限、退换货政策

用户问"红星店这个月业绩怎么样"，AI 先加载 mattress-bot skill 拿到表结构，然后才能写出正确的 SQL。没有表结构，AI 只能瞎猜字段名。

---

## 变更总结

| 组件 | 之前（s04） | 之后（s05） |
|------|------------|------------|
| 知识存储 | 无（或硬编码在 system prompt） | `skills/xxx/SKILL.md` |
| System prompt | 固定内容 | 动态注入 skill 目录 |
| 新增工具 | 无 | `load_skill` |
| Dispatch map | 4 个工具 | 5 个工具（+load_skill） |
| Agent loop | 不变 | 不变 |

**总结：知识分两层管理。目录便宜，放 system prompt 让 AI 知道有什么可用。正文贵，AI 需要时通过 load_skill 按需加载。这样 10 个 skill 只花 1000 token 的目录成本，而不是 20000 token 的全量成本。**
