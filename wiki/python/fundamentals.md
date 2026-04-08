---
title: "Guide: Python Fundamentals for Agent Development"
type: guide
category: "python/fundamentals"
kind: notes
created: 2026-04-08
updated: 2026-04-08
notes:
  - "[[python/function.md]]"
  - "[[python/dictionary.md]]"
  - "[[python/for-loop.md]]"
  - "[[python/exception-handling.md]]"
  - "[[python/decorator.md]]"
  - "[[python/generator-yield.md]]"
tags: [python, agent-development, learning-notes]
---

# Python Fundamentals for Agent Development

A focused subset of Python aimed at building LLM agents — function objects, dispatch tables, control flow, error handling, decorators, and streaming. Each note grounds the concept in an agent scenario (tool registries, retry loops, streamed LLM output) so the abstract syntax has a concrete reason to exist.

This is **not** a general Python tutorial — it's the specific shape of Python you need to build an [[agent/learn-claude-code/s01-agent-loop|agent loop]] from scratch. See the active roadmap in [[python/LEARNING-PLAN.md]].

---

## 1. Functions as objects

The foundation everything else builds on: in Python, functions are first-class values. You can pass them, store them, return them, and replace them.

- [[python/function.md|Function]] — Definition, parameters, `*args`/`**kwargs`, functions as first-class objects, returning functions, the basics that make decorators possible

## 2. Data structures for dispatch

The pattern at the heart of every agent: LLM returns a string tool name, you map it to a callable.

- [[python/dictionary.md|Dictionary]] — Key-value lookup, `dict` as a tool registry, why dispatch tables beat `if/elif` chains

## 3. Control flow

- [[python/for-loop.md|For Loop]] — `for`/`range`/`break`/`continue`, retry loops, why `return` inside a loop exits the whole function

## 4. Error handling

LLM-driven systems fail in many places. Layered exception handling keeps the agent loop alive while still propagating useful information up.

- [[python/exception-handling.md|Exception Handling]] — `try`/`except`/`finally`/`raise`, exception hierarchies, three-layer error model (tool → dispatch → agent loop bottom of stack)

## 5. Decorators

Wrap functions with cross-cutting behavior — logging, retry, registration — without touching the wrapped function's source.

- [[python/decorator.md|Decorator]] — Closures, `@` syntax, two-layer vs three-layer decorators, `@tool("name")` registration pattern, stacking decorators

## 6. Streaming

LLM responses arrive token-by-token. Generators are how Python expresses "produce values lazily over time."

- [[python/generator-yield.md|Generator / yield]] — `yield`, pause/resume semantics, streaming LLM output, why a generator beats a list for latency-sensitive output

---

## How these connect

```
LLM returns "execute_sql" string
        ↓
TOOL_REGISTRY[name]              ← dictionary (3)
        ↓ retrieves
@tool("execute_sql")             ← decorator (5) registered the function
def execute_sql(sql): ...        ← function (1)
        ↓ wrapped in @retry
for attempt in range(3):         ← for-loop (3)
    try: result = func(...)      ← exception-handling (4)
    except: ...
        ↓ result streams back
for chunk in stream: yield chunk ← generator (6)
```

Every concept earns its place by what it lets the agent do.

---

## Related

- [[wiki/python/concurrency.md|Python Concurrency]] — threads, processes, async (the next layer up)
- [[wiki/agent/learn-claude-code.md|Learn Claude Code Internals]] — the agent architecture these notes support
- [[python/LEARNING-PLAN.md]] — active learning roadmap and what's coming next
