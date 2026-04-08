---
title: "Guide: Python Concurrency for Agent Development"
type: guide
category: "python/concurrency"
kind: notes
created: 2026-04-08
updated: 2026-04-08
notes:
  - "[[python/concurrency/concurrency-overview.md]]"
  - "[[python/concurrency/threading.md]]"
  - "[[python/concurrency/thread-safety.md]]"
  - "[[python/concurrency/process.md]]"
  - "[[python/concurrency/async-await.md]]"
tags: [python, concurrency, threading, async, multiprocessing, agent-development]
---

# Python Concurrency for Agent Development

Python's three concurrency models (threads, processes, async) all solve the same problem — **blocking** — but they fit different agent scenarios. This series builds the mental model from "what is blocking" to "which model do I reach for when".

The deeper learning roadmap (event loops from scratch, IPC internals, supervisor patterns) lives in [[python/concurrency/learning-plan.md]].

---

## 1. The big picture

Pick the right model before writing any code. The overview is the decision table you'll come back to.

- [[python/concurrency/concurrency-overview.md|Concurrency Overview]] — What blocking is, the three models compared on memory/communication/risk/scenario, one-sentence room analogies, agent scenario per model

## 2. Threads — sharing memory

When the main agent needs to spawn background work (run pytest, watch a file) while staying responsive to the user, threads are the lightest option.

- [[python/concurrency/threading.md|Threading]] — `Thread`/`start`/`join`/`daemon`, fire-and-forget vs join-and-wait patterns, the agent-running-pytest-in-background canonical example

- [[python/concurrency/thread-safety.md|Thread Safety]] — Race conditions, locks, the **drain pattern** for batching notifications back to the agent loop (key for multi-tool background fan-out)

## 3. Processes — full isolation

When subagents need to be sandboxed from each other (one crash shouldn't take down the whole team), processes give you OS-level isolation at the cost of IPC overhead.

- [[python/concurrency/process.md|Process]] — Thread vs process trade-offs, IPC mechanisms (stdout/file/socket/pipe), `subprocess.run` vs `Popen`, Claude Code's parallel-agent pattern as a real example

## 4. Async — overlapping I/O on one thread

When the bottleneck is **waiting for many network calls** (LLM API + tool calls + database queries), async lets one thread overlap all the waits without the complexity of threads or processes.

- [[python/concurrency/async-await.md|Async / Await]] — `async def`/`await`/event loop, `asyncio.gather` for parallel API calls, why an event loop is the same idea as the agent React loop, when async beats threads (I/O-bound) and when it doesn't (CPU-bound)

---

## Decision table

| Need | Use |
|---|---|
| Run a slow command in the background while the agent keeps chatting | **Thread** |
| Run multiple subagents that must not crash each other | **Process** |
| Fire 10 LLM/tool API calls and wait for all in parallel | **Async** |
| Compute something CPU-heavy without blocking the agent | **Process** (not threads — GIL; not async — single-threaded) |
| Share state between executors | **Thread** (or async) |
| Isolate state between executors | **Process** |

---

## Connection to the agent loop

Every concept here maps directly to a piece of the agent architecture:

- **Background tasks** ([[agent/learn-claude-code/s08-background-tasks.md|s08]]) — threads
- **Subagents** ([[agent/learn-claude-code/s04-subagent.md|s04]]) — processes
- **Agent teams** ([[agent/learn-claude-code/s09-agent-teams.md|s09]], [[agent/learn-claude-code/s10-team-protocols.md|s10]]) — processes + IPC
- **Worktree isolation** ([[agent/learn-claude-code/s12-worktree-task-isolation.md|s12]]) — process-level isolation
- **Async tool fan-out** — `asyncio.gather` over multiple tool calls

---

## Related

- [[wiki/python/fundamentals.md|Python Fundamentals]] — function objects, decorators, exception handling (the layer below this one)
- [[wiki/agent/learn-claude-code.md|Learn Claude Code Internals]] — the agent architecture these patterns power
- [[python/concurrency/learning-plan.md]] — deep dive roadmap (event loop internals, IPC, scheduling)
