# Knowledge Vault Restructure — Multi-Layer Categories

## Overview

Redesign the vault from a flat `<vault>/raw/wiki/outputs/` structure to a **category-first, article-as-unit** structure with a top-level wiki hub.

## Current Structure (being replaced)

```
agent/
  raw/
    harness/
      2026-03-31-agent-skills.md
    assets/
  wiki/
    _index.md
    summaries/
    concepts/
  outputs/
    research/ slides/ charts/ pdfs/
```

## New Structure

```
knowledge-vault/
  _meta/
    categories.md             ← registry of all top-level categories + stats
  _templates/                 ← templates for articles, wiki guides, etc.

  wiki/                       ← curated guides hub (top-level)
    agent/
      harness.md              ← guide for agent/harness, links to articles
      memory.md
    master-courses/
      stats-inference.md
      epi.md

  agent/                      ← top-level category
    harness/                  ← sub-topic
      agent-skills/           ← article unit (atomic)
        article.md            ← the ingested source
        assets/               ← images, PDFs, media for this article
        slides.md             ← optional: generated Marp slides
        research.md           ← optional: Q&A output
        chart.png             ← optional: generated chart
      qoder-harness/
        article.md
        assets/
    memory/
      some-article/
        article.md
        assets/

  master-courses/             ← top-level category
    stats-inference/          ← sub-topic
      lecture-1/
        article.md
        assets/
    epi/
      intro-to-epi/
        article.md
        assets/
```

## Design Decisions

### Article Unit (atomic/minimal unit)
- A folder named with a slug (e.g. `agent-skills/`)
- Always contains `article.md` — the ingested source content
- Always contains `assets/` — downloaded images, PDFs, media
- May contain outputs: `slides.md`, `research.md`, `chart.png`, etc.
- Self-contained: everything about one source lives together

### Categories (organizational layers)
- Pure folders — no special files required, just nesting
- Can be N levels deep (e.g. `master-courses/stats-inference/module-3/lecture-1/`)
- No `raw/`, `wiki/`, `outputs/` separation within categories

### Wiki Hub (top-level)
- Lives at `wiki/` at the vault root
- Mirrors the category tree structure
- Each `.md` file is a curated guide for a sub-topic
- Contains synthesis, key takeaways, and `[[links]]` to articles
- Example: `wiki/agent/harness.md` links to `[[agent/harness/agent-skills/article.md]]`

### Category Registry (`_meta/categories.md`)
- Replaces `_meta/vaults.md`
- Tracks top-level categories with descriptions and article counts

## Frontmatter Schemas

### Article (`<category>/<sub>/<slug>/article.md`)
```yaml
---
title: "Article Title"
source: "https://original-url"
platform: "web|arxiv|youtube|github|twitter|xiaohongshu|wechat|bilibili"
author: "Author Name"
date: YYYY-MM-DD
ingested: YYYY-MM-DDTHH:MM:SSZ
tags: [tag1, tag2]
category: "agent/harness"
compiled: false
---
```

### Wiki Guide (`wiki/<category>/<sub-topic>.md`)
```yaml
---
title: "Guide: Harness Patterns"
type: guide
category: "agent/harness"
created: YYYY-MM-DD
updated: YYYY-MM-DD
articles:
  - "[[agent/harness/agent-skills/article.md]]"
  - "[[agent/harness/qoder-harness/article.md]]"
tags: [agent, harness]
---
```

## Workflows

### Ingest
1. User provides URL + category path (e.g. "ingest into agent/harness")
2. Fetch content, convert to markdown
3. Create article folder: `agent/harness/<slug>/`
4. Download assets to `agent/harness/<slug>/assets/`
5. Save `article.md` with frontmatter (`compiled: false`)

### Compile
1. Find all `article.md` files with `compiled: false`
2. For each: update or create the wiki guide at `wiki/<category>/<sub-topic>.md`
3. Set `compiled: true`
4. Update `_meta/categories.md` counts

### Q&A
1. Search across wiki guides and articles using Grep/Glob
2. Synthesize answer with `[[wiki-links]]` citations
3. Optionally save output as `research.md` inside a relevant article folder, or as a standalone article unit

### Generate Outputs
- Slides, charts, PDFs are saved inside the relevant article folder alongside `article.md`
- Cross-article outputs (spanning multiple articles) get their own article-level folder

## Migration

1. Move `agent/raw/harness/2026-03-31-agent-skills.md` → `agent/harness/agent-skills/article.md`
2. Move `agent/raw/harness/2026-04-03-qoder-harness.md` → `agent/harness/qoder-harness/article.md`
3. Move assets into per-article `assets/` folders
4. Remove old `agent/raw/`, `agent/wiki/`, `agent/outputs/` structure
5. Create `wiki/agent/harness.md` guide
6. Rename `_meta/vaults.md` → `_meta/categories.md`
7. Update `CLAUDE.md` with new conventions
8. Update templates

## What Stays the Same

- `_meta/` and `_templates/` at root
- Obsidian wiki-link conventions
- Claude Code as sole operator
- ISO dates, slug conventions
