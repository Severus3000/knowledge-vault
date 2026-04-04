# Knowledge Vault — Claude Code Instructions

This is an Obsidian-native, multi-vault knowledge base. You (Claude Code) are the sole LLM operator. The user views everything in Obsidian and never manually edits the wiki. You maintain all data.

## Vault Structure

Each knowledge base is a top-level folder:

```
<vault-name>/
├── raw/
│   ├── assets/                  ← downloaded images, PDFs, media
│   └── YYYY-MM-DD-<slug>.md    ← ingested sources
├── wiki/
│   ├── _index.md               ← auto-maintained master index
│   ├── summaries/              ← one summary per raw source
│   └── concepts/               ← categorized concept articles
└── outputs/
    ├── research/               ← Q&A results filed back
    ├── slides/                 ← Marp presentations
    ├── charts/                 ← matplotlib/mermaid images
    └── pdfs/                   ← generated PDFs
```

Shared directories:
- `_templates/` — markdown templates for all file types
- `_meta/vaults.md` — registry of all vaults with descriptions and stats

## Conventions

- Use Obsidian wiki-links: `[[path/to/file.md]]` and `![[assets/image.png]]`
- Cross-vault links: `[[other-vault/wiki/concepts/foo.md]]`
- All dates in ISO format: `YYYY-MM-DD`
- Slugs: lowercase, hyphens, no special characters
- Never overwrite raw sources — they are immutable once ingested
- Always update `wiki/_index.md` and `_meta/vaults.md` after compilation

## Frontmatter Schemas

### Raw Source
```yaml
---
title: "Article Title"
source: "https://original-url"
platform: "web|arxiv|youtube|github|twitter|xiaohongshu|wechat|bilibili"
author: "Author Name"
date: YYYY-MM-DD
ingested: YYYY-MM-DDTHH:MM:SSZ
tags: [tag1, tag2]
compiled: false
---
```

### Wiki Summary
```yaml
---
title: "Summary: Article Title"
type: summary
source: "[[raw/YYYY-MM-DD-slug.md]]"
created: YYYY-MM-DD
tags: [tag1, tag2]
---
```

### Wiki Concept
```yaml
---
title: "Concept Name"
type: concept
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - "[[raw/source-a.md]]"
  - "[[raw/source-b.md]]"
related:
  - "[[concepts/related-topic.md]]"
tags: [tag1, tag2]
---
```

### Output (Research, Slides, etc.)
```yaml
---
title: "Research: Question" | "Slides: Topic"
date: YYYY-MM-DD
vault_sources:
  - "[[wiki/concepts/foo.md]]"
tags: [research|slides|chart]
---
```

## Workflow: Create a New Vault

1. Create all subdirectories: `<name>/raw/assets/`, `<name>/wiki/summaries/`, `<name>/wiki/concepts/`, `<name>/outputs/research/`, `<name>/outputs/slides/`, `<name>/outputs/charts/`, `<name>/outputs/pdfs/`
2. Create `<name>/wiki/_index.md` from `_templates/wiki-index.md`
3. Add entry to `_meta/vaults.md`

## Workflow: Ingest a Source

1. Fetch URL content (use web-access tools)
2. Convert to clean markdown
3. Download images to `<vault>/raw/assets/`, rewrite refs to `![[assets/<filename>]]`
4. Save to `<vault>/raw/YYYY-MM-DD-<slug>.md` using `_templates/raw-source.md` frontmatter
5. Set `compiled: false`

## Workflow: Compile

1. Read `<vault>/wiki/_index.md` for current state
2. Find files with `compiled: false` in `<vault>/raw/`
3. For each uncompiled source:
   a. Read the raw content
   b. Write a summary to `wiki/summaries/<slug>.md`
   c. Determine concept category — create or update `wiki/concepts/<slug>.md`
   d. Set `compiled: true` in the raw file frontmatter
4. Update `wiki/_index.md` with new entries and stats
5. Update `_meta/vaults.md` counts

## Workflow: Q&A

1. Read `<vault>/wiki/_index.md` for overview
2. Grep/Glob for relevant articles
3. Read and synthesize an answer with `[[wiki-links]]` citations
4. If user wants to keep the answer: save to `outputs/research/YYYY-MM-DD-<slug>.md`

## Workflow: Generate Outputs

- **Marp slides**: Write to `outputs/slides/<name>.md` in Marp format
- **Charts**: Generate via matplotlib (save .png to `outputs/charts/`) or mermaid (inline in markdown)
- **PDFs**: Generate markdown then convert via `pandoc` CLI to `outputs/pdfs/`
- **Research**: Save Q&A results to `outputs/research/`

## Index Format

`wiki/_index.md` should follow this structure:

```markdown
# <Vault Name> — Wiki Index

> Last compiled: YYYY-MM-DD

## Topics
- **Category**: [[concepts/slug.md]] — one-line summary

## Recent
- YYYY-MM-DD: Compiled [[raw/source.md]] → [[summaries/slug.md]]

## Stats
- Raw sources: N (M uncompiled)
- Wiki articles: X concepts, Y summaries
```
