# Knowledge Vault

A personal Obsidian-native knowledge base operated by Claude Code. Articles get **ingested** from external sources (papers, videos, blog posts, course PDFs) and notes get **self-authored** as I learn. Claude Code is the sole writer — I view everything in Obsidian and never manually edit the wiki.

Inspired by [Karpathy's LLM Knowledge Bases](https://x.com/karpathy/status/1936469592498032744) approach.

## Two content types

The vault recognizes two first-class content types:

| | **Article** | **Note** |
|---|---|---|
| Origin | Ingested from external source | Self-authored as I learn |
| Mutability | Immutable once ingested | Mutable — keeps evolving |
| Granularity | One source = one article | Many notes = one series |
| Folder shape | `<slug>/article.md` + `assets/` | flat `<series>/<note-name>.md` |

See [`CLAUDE.md`](CLAUDE.md) for the full content model and workflows.

## Structure

```
knowledge-vault/
├── _meta/categories.md      # Registry of all categories with type + count
├── _templates/              # Markdown templates for articles, guides, outputs
├── CLAUDE.md                # Instructions for Claude Code (the sole operator)
│
├── wiki/                    # Curated guides — the navigation hub
│   ├── agent/
│   │   ├── harness.md
│   │   └── learn-claude-code.md
│   ├── python/
│   │   ├── fundamentals.md
│   │   └── concurrency.md
│   └── master-courses/
│       ├── longitudinal-data-analysis.md
│       └── epidemiology.md
│
├── agent/                   # Category: AI agent engineering
│   ├── harness/             # Article series (ingested)
│   │   └── <slug>/article.md + assets/
│   ├── memory/              # Article series (ingested)
│   └── learn-claude-code/   # Note series (self-authored, s01-s12)
│       └── s01-agent-loop.md, s02-tool-use.md, ...
│
├── python/                  # Category: Python for agent dev
│   ├── *.md                 # Note series (self-authored fundamentals)
│   └── concurrency/         # Note series (threads, async, processes)
│
└── master-courses/          # Category: graduate coursework
    └── <course>/<topic>/<slug>/article.md + assets/
```

## Setup

1. Open this folder as an [Obsidian](https://obsidian.md) vault
2. Recommended Obsidian community plugins: **Marp Slides**, **Dataview**
3. Install [Claude Code](https://docs.anthropic.com/en/docs/claude-code) and set `ANTHROPIC_API_KEY`
4. Optional: install [pandoc](https://pandoc.org/installing.html) for PDF generation

## Usage

Everything runs through prompts to Claude Code in this directory:

```
# Ingest a source
"Ingest https://arxiv.org/abs/2501.xxxxx into agent/memory"
"Ingest this PDF into master-courses/longitudinal-data-analysis"

# Compile (link new articles into wiki guides)
"Compile the agent/harness wiki"

# Q&A across the vault
"What do I know about ReAct agents? Cite sources."
"How does multilevel growth modeling handle missing data?"

# Generate outputs
"Make a Marp deck from the openclaw article"
"Write a research note synthesizing all my MLE/REML articles"
```

## Conventions

- **Wiki-links** — `[[category/sub/slug/article.md]]` for articles, `[[note-name]]` for notes (Obsidian basename indexing handles paths)
- **Slugs** — lowercase, hyphenated, no special characters
- **Dates** — ISO format (`YYYY-MM-DD`)
- **Articles are immutable** once ingested; **notes are mutable** as understanding deepens
- **Wiki guides and `_meta/categories.md`** stay in sync after every change

## License

Content I authored (notes, wiki guides, README, CLAUDE.md): MIT.
Ingested third-party sources (articles, PDFs, course materials) retain their original copyright and licenses — they live here as personal study material, not for redistribution.
