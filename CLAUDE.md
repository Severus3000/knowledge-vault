# Knowledge Vault — Claude Code Instructions

This is an Obsidian-native knowledge base with multi-layer categories. You (Claude Code) are the sole LLM operator. The user views everything in Obsidian and never manually edits the wiki. You maintain all data.

## Structure

```
knowledge-vault/
  _meta/categories.md         ← registry of all categories + stats
  _templates/                 ← markdown templates

  wiki/                       ← curated guides hub (top-level)
    <category>/
      <sub-topic>.md          ← guide with links to articles

  <category>/                 ← top-level category (e.g. agent, master-courses)
    <sub-topic>/              ← sub-topic (e.g. harness, stats-inference)
      <article-slug>/         ← article unit (atomic, minimal unit)
        article.md            ← the ingested source
        assets/               ← images, PDFs, media for this article
        slides.md             ← optional: generated Marp slides
        research.md           ← optional: Q&A output
        chart.png             ← optional: generated chart
```

### Key Concepts
- **Article unit** = the atomic unit. A folder containing `article.md` + `assets/` + optional outputs
- **Categories** = pure organizational nesting (folders). Can be N levels deep
- **Wiki** = top-level hub at `wiki/`. Mirrors category tree. Each file is a curated guide linking to articles
- **`_meta/categories.md`** = tracks all categories with descriptions and article counts

Shared directories:
- `_templates/` — markdown templates for articles, wiki guides, outputs
- `_meta/categories.md` — category registry

## Conventions

- Use Obsidian wiki-links: `[[path/to/article.md]]` and `![[assets/image.png]]`
- Cross-category links: `[[other-category/sub/slug/article.md]]`
- All dates in ISO format: `YYYY-MM-DD`
- Slugs: lowercase, hyphens, no special characters
- Never overwrite ingested articles — they are immutable once ingested
- Always update wiki guides and `_meta/categories.md` after compilation

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
category: "category/sub-topic"
compiled: false
---
```

### Wiki Guide (`wiki/<category>/<sub-topic>.md`)
```yaml
---
title: "Guide: Topic Name"
type: guide
category: "category/sub-topic"
created: YYYY-MM-DD
updated: YYYY-MM-DD
articles:
  - "[[category/sub/slug-a/article.md]]"
  - "[[category/sub/slug-b/article.md]]"
tags: [tag1, tag2]
---
```

### Output (inside article unit)
```yaml
---
title: "Research: Question" | "Slides: Topic"
date: YYYY-MM-DD
source_article: "[[category/sub/slug/article.md]]"
tags: [research|slides|chart]
---
```

## Workflow: Create a New Category

1. Create the category folder: `<category>/<sub-topic>/`
2. Create wiki guide: `wiki/<category>/<sub-topic>.md`
3. Add entry to `_meta/categories.md`

## Workflow: Ingest a Source

1. User provides URL + category path (e.g. "ingest into agent/harness")
2. Fetch URL content (use web-access tools)
3. Convert to clean markdown
4. Create article folder: `<category>/<sub>/<slug>/`
5. Download images to `<category>/<sub>/<slug>/assets/`, rewrite refs to `![[assets/<filename>]]`
6. Save `article.md` with frontmatter (`compiled: false`)

## Workflow: Compile

1. Find all `article.md` files with `compiled: false` (use Grep)
2. For each uncompiled article:
   a. Read the content
   b. Update or create the wiki guide at `wiki/<category>/<sub-topic>.md`
   c. Add key takeaways, synthesis, and article link to the guide
   d. Set `compiled: true` in the article frontmatter
3. Update `_meta/categories.md` counts

## Workflow: Q&A

1. Search across wiki guides and articles using Grep/Glob
2. Read and synthesize an answer with `[[wiki-links]]` citations
3. If user wants to keep the answer: save as `research.md` inside the most relevant article folder
4. For cross-article research: create a new article-level folder for the output

## Workflow: Generate Outputs

- **Marp slides**: Save as `slides.md` inside the relevant article folder
- **Charts**: Generate via matplotlib (save .png to the article folder) or mermaid (inline)
- **PDFs**: Generate markdown then convert via `pandoc` CLI, save inside article folder
- **Cross-article outputs**: Create a dedicated folder at the appropriate category level
