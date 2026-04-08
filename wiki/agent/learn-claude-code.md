---
title: "Guide: Learn Claude Code Internals"
type: guide
category: "agent/learn-claude-code"
kind: notes
created: 2026-04-08
updated: 2026-04-08
notes:
  - "[[agent/learn-claude-code/s01-agent-loop.md]]"
  - "[[agent/learn-claude-code/s02-tool-use.md]]"
  - "[[agent/learn-claude-code/s03-todo-write.md]]"
  - "[[agent/learn-claude-code/s04-subagent.md]]"
  - "[[agent/learn-claude-code/s05-skill-loading.md]]"
  - "[[agent/learn-claude-code/s06-context-compact.md]]"
  - "[[agent/learn-claude-code/s07-task-system.md]]"
  - "[[agent/learn-claude-code/s08-background-tasks.md]]"
  - "[[agent/learn-claude-code/s09-agent-teams.md]]"
  - "[[agent/learn-claude-code/s10-team-protocols.md]]"
  - "[[agent/learn-claude-code/s11-autonomous-agents.md]]"
  - "[[agent/learn-claude-code/s12-worktree-task-isolation.md]]"
tags: [agent, claude-code, agent-loop, react, multi-agent, learning-notes]
---

# Learn Claude Code Internals

A 12-session walkthrough of how Claude Code (and any modern coding agent) actually works under the hood — from the 30-line ReAct loop in `s01` up through agent teams and worktree isolation in `s12`. Each session adds **one mechanism** to the previous one without rewriting what came before, so by the end you've watched a full agent harness assemble itself.

The series breaks at `s06 | s07` — the first half is **single-agent foundations**, the second half is **multi-agent and isolation**.

```
s01 > s02 > s03 > s04 > s05 > s06 | s07 > s08 > s09 > s10 > s11 > s12
└──────── single agent ────────┘ └────── teams + isolation ──────┘
```

---

## Part 1 — Single agent foundations (s01-s06)

How a single agent stays useful as it grows from 30 lines to a real harness.

- [[agent/learn-claude-code/s01-agent-loop.md|s01 — Agent Loop]] — *"One loop & Bash is all you need"* — the 30-line ReAct loop, message history as state, why `stop_reason` controls exit
- [[agent/learn-claude-code/s02-tool-use.md|s02 — Tool Use]] — *"加一个工具，只加一个 handler"* — dispatch map replaces `if/elif`, path sandboxing, why dedicated tools beat one bash everywhere
- [[agent/learn-claude-code/s03-todo-write.md|s03 — TodoWrite]] — *"没有计划的 agent 走哪算哪"* — explicit planning before action, completion rates double when the agent writes its own todo list
- [[agent/learn-claude-code/s04-subagent.md|s04 — Subagent]] — *"大任务拆小，每个小任务干净的上下文"* — disposable subagents protect the main context window, parent stays sharp
- [[agent/learn-claude-code/s05-skill-loading.md|s05 — Skill Loading]] — *"用到什么知识，临时加载什么知识"* — directory in system prompt is cheap, body content loaded on demand, skill metadata vs full content
- [[agent/learn-claude-code/s06-context-compact.md|s06 — Context Compact]] — *"上下文总会满，要有办法腾地方"* — compaction strategy, swap-to-disk vs lossy summarization, what to keep and what to drop

## Part 2 — Multi-agent and isolation (s07-s12)

When one agent isn't enough — task systems, background work, and how agents coordinate without stepping on each other.

- [[agent/learn-claude-code/s07-task-system.md|s07 — Task System]] — *"大目标要拆成小任务，排好序，记在磁盘上"* — task graph that outlives any single conversation, dependencies, persistence
- [[agent/learn-claude-code/s08-background-tasks.md|s08 — Background Tasks]] — *"慢操作丢后台，agent 继续想下一步"* — fire-and-forget I/O via [[python/concurrency/threading.md|threads]], notification drain pattern
- [[agent/learn-claude-code/s09-agent-teams.md|s09 — Agent Teams]] — *"任务太大一个人干不完，要能分给队友"* — multi-agent fan-out, file-based IPC over shared memory, [[python/concurrency/process.md|processes]] not threads
- [[agent/learn-claude-code/s10-team-protocols.md|s10 — Team Protocols]] — *"队友之间要有统一的沟通规矩"* — structured message protocol replaces free-text coordination, schemas keep agents aligned
- [[agent/learn-claude-code/s11-autonomous-agents.md|s11 — Autonomous Agents]] — *"队友自己看看板，有活就认领"* — kanban-style work queue, agents self-assign, WORK/IDLE state machine
- [[agent/learn-claude-code/s12-worktree-task-isolation.md|s12 — Worktree + Task Isolation]] — *"各干各的目录，互不干扰"* — task ID bound to git worktree, OS-level filesystem isolation between agents

---

## Reading order

The breadcrumb at the top of each note (`s01 > s02 > [ s03 ] s04 > ...`) shows where you are in the sequence. Each session builds on the previous ones — you can skip around but the harness only makes sense end-to-end.

If you only have time for the most load-bearing four:
1. **s01** — the loop itself (everything else is layers on top)
2. **s02** — dispatch map (the abstraction every later session relies on)
3. **s04** — subagents (the first context-window protection technique)
4. **s09** — agent teams (the leap from one agent to many)

---

## Connection to Python concurrency

The CS background that makes the second half (s07-s12) click lives in the python concurrency series:

| Session | Python concept |
|---|---|
| s08 — Background Tasks | [[python/concurrency/threading.md|threading]] + [[python/concurrency/thread-safety.md|drain pattern]] |
| s09 — Agent Teams | [[python/concurrency/process.md|process]] + IPC |
| s10 — Team Protocols | [[python/concurrency/process.md|process]] (structured stdio) |
| s12 — Worktree Isolation | [[python/concurrency/process.md|process]]-level isolation |
| s01 / s08 (event loop) | [[python/concurrency/async-await.md|async/await]] |

Read [[python/concurrency/learning-plan.md]] for the deep dive roadmap into the OS/CS internals behind these patterns.

---

## Related

- [[wiki/agent/harness.md|Agent Harness Engineering]] — how to make an agent reliable in a real codebase (validation, AGENTS.md, self-iteration)
- [[wiki/python/fundamentals.md|Python Fundamentals]] — the language layer (functions, dispatch, decorators) these sessions assume
- [[wiki/python/concurrency.md|Python Concurrency]] — the threading/async/process primitives the multi-agent half is built on
