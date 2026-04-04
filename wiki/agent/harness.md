---
title: "Guide: Agent Harness Engineering"
type: guide
category: "agent/harness"
created: 2026-04-04
updated: 2026-04-04
articles:
  - "[[agent/harness/agent-skills/article.md]]"
  - "[[agent/harness/qoder-harness/article.md]]"
tags: [agent, harness, coding-agent, skills]
---

# Agent Harness Engineering

Harness 工程是一套让 AI Agent 在代码仓库中可靠工作的方法论。核心思想：与其教 Agent 怎么做，不如让它自己验证做得对不对。

## Key Concepts

- **仓库即操作系统** — 所有规则编码到仓库中，Agent 才能看见
- **AGENTS.md 是地图不是手册** — 控制在 ~100 行，指路而非穷举
- **机械化验证** — lint、test、verify 组成验证管道，不靠 LLM 直觉
- **事前预防优于事后修复** — 写代码前先验证操作是否合法
- **协调者不写代码** — 拆分 Coordinator / Executor，保护上下文窗口
- **Harness 自我进化** — 失败记录 → Critic 分析 → Refiner 更新规则

## Articles

- [[agent/harness/agent-skills/article.md]] — Agent Skills 标准：可复用专业领域知识的封装与生态
- [[agent/harness/qoder-harness/article.md]] — Qoder Harness Engineering 实践指南：验证管道、上下文管理、反馈循环
