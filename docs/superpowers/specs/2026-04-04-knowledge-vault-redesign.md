# Knowledge Vault Redesign — LLM Knowledge Base

## Overview

Complete redesign of knowledge-vault from a web app with custom agents into an Obsidian-native, multi-vault knowledge base operated entirely by Claude Code. No backend, no frontend, no custom agents, no CLI, no MCP server. Just a well-structured vault on the filesystem that Claude Code reads/writes directly and the user views in Obsidian.

Inspired by Karpathy's LLM Knowledge Base pattern: raw data collected from sources → compiled by LLM into a markdown wiki → operated on by LLM for Q&A, outputs, and incremental enhancement → all viewable in Obsidian.

## What Gets Deleted

All existing code is removed:

- `server/` — FastAPI backend, agents, services, APIs, CLI, MCP server
- `web/` — React frontend
- `tests/` — test suite for the above
- `pyproject.toml` — Python project config
- `.env.example`
- `knowledge_vault.egg-info/`

## What Gets Created

A pure filesystem-based knowledge vault with Obsidian configuration and a CLAUDE.md that teaches Claude Code how to operate on it.

## Architecture

```
knowledge-vault/                    ← git repo + Obsidian vault root
├── .obsidian/                      ← Obsidian config, plugins, themes
├── CLAUDE.md                       ← master instructions for Claude Code
├── _templates/                     ← markdown templates (raw, wiki, output)
│   ├── raw-source.md
│   ├── wiki-summary.md
│   ├── wiki-concept.md
│   ├── output-research.md
│   └── output-slides.md
├── _meta/
│   └── vaults.md                   ← registry of all vaults + descriptions
├── <vault-name>/                   ← one per knowledge base (top-level)
│   ├── raw/
│   │   ├── assets/                 ← downloaded images, PDFs, media
│   │   └── YYYY-MM-DD-<slug>.md   ← ingested sources
│   ├── wiki/
│   │   ├── _index.md              ← auto-maintained master index
│   │   ├── summaries/             ← one per raw source
│   │   └── concepts/              ← categorized concept articles
│   └── outputs/
│       ├── research/              ← Q&A results filed back into vault
│       ├── slides/                ← Marp-format presentations
│       ├── charts/                ← matplotlib/mermaid images
│       └── pdfs/                  ← generated PDF files
└── <another-vault>/
    ├── raw/
    ├── wiki/
    └── outputs/
```

Vaults are top-level folders for flat Obsidian navigation. Meta directories use `_` prefix to sort first and stay out of the way.

## Data Model

### Raw Source (`<vault>/raw/YYYY-MM-DD-<slug>.md`)

```yaml
---
title: "Article Title"
source: "https://original-url"
platform: "web|arxiv|youtube|github|twitter|xiaohongshu|wechat|bilibili"
author: "Author Name"
date: 2026-04-01
ingested: 2026-04-04T10:00:00Z
tags: [tag1, tag2]
compiled: false
---

# Article content in markdown

Images referenced as: ![[assets/image-name.png]]
```

- `compiled: false` — flipped to `true` after Claude Code compiles this source into wiki articles
- `assets/` stores downloaded images, referenced via Obsidian embed syntax
- Filename uses ingestion date + slugified title for uniqueness and chronological sorting

### Wiki Summary (`<vault>/wiki/summaries/<slug>.md`)

One per raw source. Short summary + categorization.

```yaml
---
title: "Summary: Article Title"
type: summary
source: "[[raw/2026-04-01-article.md]]"
created: 2026-04-04
tags: [tag1, tag2]
---

Brief summary of key points from the source.

## Key Takeaways
- Point 1
- Point 2

## Category
Categorized under: [[concepts/category-name.md]]
```

### Wiki Concept (`<vault>/wiki/concepts/<slug>.md`)

Synthesized articles that group knowledge from multiple sources.

```yaml
---
title: "Concept Name"
type: concept
created: 2026-04-04
updated: 2026-04-04
sources:
  - "[[raw/2026-04-01-article-a.md]]"
  - "[[raw/2026-04-02-article-b.md]]"
related:
  - "[[concepts/related-topic.md]]"
tags: [tag1, tag2]
---

Synthesized knowledge about this concept, drawn from multiple sources.
Uses Obsidian wiki-links for cross-references: [[concepts/other.md]]
```

### Wiki Index (`<vault>/wiki/_index.md`)

Auto-maintained by Claude Code during compilation. Serves as the entry point for both human browsing and Claude Code's own lookups.

```markdown
# <Vault Name> — Wiki Index

> Last compiled: 2026-04-04

## Topics
- **Category A**: [[concepts/foo.md]] — one-line summary
- **Category B**: [[concepts/bar.md]] — one-line summary

## Recent
- 2026-04-04: Compiled [[raw/2026-04-04-new-article.md]] → [[summaries/new-article.md]]

## Stats
- Raw sources: 42 (3 uncompiled)
- Wiki articles: 28 concepts, 42 summaries
```

### Vault Registry (`_meta/vaults.md`)

```markdown
# Knowledge Vaults

| Vault | Description | Sources | Articles |
|-------|-------------|---------|----------|
| [[llm-agents/wiki/_index.md\|llm-agents]] | LLM agent architectures and frameworks | 42 | 28 |
| [[robotics/wiki/_index.md\|robotics]] | Robotics research and embodied AI | 15 | 10 |
```

Auto-maintained by Claude Code when vaults are created or compiled.

### Output Files

**Research** (`outputs/research/YYYY-MM-DD-<query-slug>.md`):
```yaml
---
title: "Research: <question>"
date: 2026-04-04
vault_sources:
  - "[[wiki/concepts/foo.md]]"
  - "[[wiki/concepts/bar.md]]"
tags: [research]
---

Synthesized answer to the question, with citations back to wiki articles.
```

**Slides** (`outputs/slides/<name>.md`): Marp-format markdown, viewable in Obsidian with Marp plugin.

**Charts** (`outputs/charts/<name>.png`): Generated via matplotlib or mermaid, embedded in other documents via `![[charts/name.png]]`.

**PDFs** (`outputs/pdfs/<name>.pdf`): Generated from markdown via pandoc or similar.

## Workflows

All workflows are driven by prompting Claude Code in natural language. No custom code.

### 1. Create a New Vault

User: "Create a new vault for quantum computing"

Claude Code:
1. Creates `quantum-computing/raw/`, `quantum-computing/raw/assets/`, `quantum-computing/wiki/`, `quantum-computing/wiki/summaries/`, `quantum-computing/wiki/concepts/`, `quantum-computing/outputs/research/`, `quantum-computing/outputs/slides/`, `quantum-computing/outputs/charts/`, `quantum-computing/outputs/pdfs/`
2. Creates `quantum-computing/wiki/_index.md` with empty template
3. Updates `_meta/vaults.md` registry

### 2. Ingest a Source

User: "Ingest https://example.com/article into the llm-agents vault"

Claude Code:
1. Fetches the URL content (via web-access tools)
2. Converts to clean markdown
3. Downloads referenced images to `llm-agents/raw/assets/`
4. Rewrites image references to `![[assets/<filename>]]`
5. Saves to `llm-agents/raw/YYYY-MM-DD-<slug>.md` with frontmatter (`compiled: false`)

### 3. Compile Raw → Wiki

User: "Compile the llm-agents vault"

Claude Code:
1. Reads `llm-agents/wiki/_index.md` for current state
2. Finds uncompiled raw files (frontmatter `compiled: false`)
3. For each uncompiled source:
   - Reads the raw content
   - Writes a summary to `wiki/summaries/<slug>.md`
   - Determines which concept(s) the source belongs to
   - Creates new concept articles or updates existing ones in `wiki/concepts/`
   - Sets `compiled: true` in the raw file's frontmatter
4. Updates `wiki/_index.md` with new entries, summaries, and stats
5. Updates `_meta/vaults.md` with new counts

### 4. Q&A

User: "What do I know about transformer architectures? Check the llm-agents vault."

Claude Code:
1. Reads `llm-agents/wiki/_index.md` to understand what's available
2. Uses Grep/Glob to find relevant articles
3. Reads the relevant concept articles and summaries
4. Synthesizes an answer with `[[wiki-links]]` as citations
5. Optionally files the answer to `outputs/research/` if user wants to keep it

### 5. Generate Outputs

User: "Create a Marp presentation about attention mechanisms from the llm-agents vault"

Claude Code:
1. Researches the topic in the vault
2. Generates Marp-format markdown in `outputs/slides/attention-mechanisms.md`
3. Any generated charts go to `outputs/charts/` and are embedded

User: "Generate a PDF summary of my robotics vault"

Claude Code:
1. Reads the vault wiki
2. Generates a comprehensive markdown document
3. Converts to PDF via `pandoc` CLI (must be installed on system), saves to `outputs/pdfs/`

### 6. File Outputs Back

User: "File that research back into the wiki"

Claude Code moves/links the output from `outputs/research/` into the wiki structure, updating `_index.md` and relevant concept articles.

## CLAUDE.md Design

The `CLAUDE.md` at the repo root is the core of the system — it teaches Claude Code how to operate the vault. It contains:

1. **Vault structure conventions** — directory layout, naming patterns
2. **Frontmatter schemas** — required fields for raw, summary, concept, output files
3. **Compilation instructions** — how to find uncompiled sources, what to generate, how to update the index
4. **Template references** — points to `_templates/` for consistent file creation
5. **Obsidian conventions** — use `[[wiki-links]]` and `![[embeds]]`, not standard markdown links
6. **Cross-vault linking** — how to reference across vaults: `[[other-vault/wiki/concepts/foo.md]]`

This is not code — it's structured natural language instructions that Claude Code follows.

## Obsidian Configuration

### Required Plugins
- **Marp Slides** — render slide presentations
- **Dataview** — query frontmatter for dashboards (optional but useful)
- **Graph Analysis** — filter graph view by folder/vault

### Obsidian Settings
- Vault root: the repo root (`knowledge-vault/`)
- Default new file location: not relevant (Claude Code handles all file creation)
- Wiki-link format: shortest path when possible
- Attachment folder: per-vault `raw/assets/`

### `.obsidian/` Contents
- `app.json` — core settings
- `community-plugins.json` — plugin list
- `graph.json` — graph view filters (can filter by vault folder)
- `templates.json` — template folder set to `_templates/`

## What This Design Does NOT Include

- **No backend/server** — Claude Code reads/writes the filesystem directly
- **No custom agents** — Claude Code is the agent
- **No CLI tools** — Claude Code has Bash, Read, Write, Grep, Glob
- **No MCP server** — unnecessary when Claude Code operates directly
- **No database** — the filesystem IS the database, frontmatter IS the schema
- **No search engine** — Claude Code's Grep + the wiki index is sufficient at this scale
- **No web UI** — Obsidian is the UI
- **No tests** — nothing to test, there's no code (CLAUDE.md instructions are validated by usage)

## Migration Plan

1. Delete: `server/`, `web/`, `tests/`, `pyproject.toml`, `.env.example`, `knowledge_vault.egg-info/`, `vault/` (empty anyway)
2. Create: directory structure, `_templates/`, `_meta/`, `.obsidian/` config
3. Write: `CLAUDE.md` with full vault operation instructions
4. Write: `README.md` with setup instructions (install Obsidian, open vault, install plugins)
5. Update: `.gitignore` for Obsidian workspace files and OS files
