---
name: knowledge-vault
description: Use when user says "save to vault", "add to knowledge vault", "check vault for X", "归档到知识库", or when you notice content worth archiving (a useful article, research finding, or paper the user is reading). Teaches you how to ingest into and query Rui's Obsidian knowledge vault from ANY working directory.
---

# Knowledge Vault — External AI Manual

You are NOT inside the knowledge vault directory. This skill teaches you how to reach in safely from wherever you are.

**Vault path:** `/Users/rui/Desktop/knowledge-vault/`
**Canonical rules (if in doubt):** `/Users/rui/Desktop/knowledge-vault/CLAUDE.md`

## Hard Boundaries — What You CANNOT Do

External AI (you, right now) is **ingest + query only**. These are forbidden:

- **Never touch `wiki/`** — that's the curated hub, managed only from inside the vault by Claude Code running in that directory.
- **Never compile articles** — you leave new articles with `compiled: false`; compilation happens later, inside the vault.
- **Never update `_meta/categories.md`** — only inside-the-vault Claude touches the registry.
- **Never overwrite an existing `article.md`** — articles are immutable once ingested.
- **Never create notes** (self-authored learning notes) from outside — notes belong to study sessions inside the vault.

You may create ONE thing: a new article folder under an existing category. That's it.

## When to Invoke This Skill

**Explicit commands (always act):**
- "save this to vault" / "add to knowledge vault" / "归档到知识库"
- "check vault for X" / "does vault have anything on Y"
- "ingest this into <category>"

**Proactive suggestion (ask first, never auto-write):**
When user has clearly engaged with external content worth preserving — reading a paper, researching a technique, bookmarking an article — offer:
> "Want me to save this to your knowledge vault?"

Do NOT suggest for:
- Ephemeral project-specific debugging
- Generated code or tool output
- Anything already in the current project's own docs
- Your own explanations (vault is for sources, not for AI output)

## Workflow A: Query (read-only)

User asks "does the vault have anything on X?" or "what did I save about Y?":

1. **Check categories first** — Read `/Users/rui/Desktop/knowledge-vault/_meta/categories.md` to see what topic areas exist.
2. **Grep articles** — Search article frontmatter and content:
   ```
   Grep pattern="<search term>" path="/Users/rui/Desktop/knowledge-vault" glob="**/article.md"
   ```
3. **Grep wiki guides** for synthesized answers:
   ```
   Grep pattern="<search term>" path="/Users/rui/Desktop/knowledge-vault/wiki"
   ```
4. **Report with wiki-link citations** in Obsidian format: `[[category/sub/slug/article.md]]`.
5. **Do not modify anything.**

## Workflow B: Ingest (create one article)

User wants to save a URL/source to the vault. Steps in order:

### Step 1: Determine category

- Read `/Users/rui/Desktop/knowledge-vault/_meta/categories.md` to see existing categories.
- Pick the best existing `<category>/<sub-topic>` match.
- **If no good fit exists:** STOP and ask the user which category to use, or whether to create a new one. Do NOT silently create new categories from outside — ask first.

### Step 2: Duplicate check (MANDATORY)

Before fetching or writing anything:

```
Grep pattern="<source URL>" path="/Users/rui/Desktop/knowledge-vault" glob="**/article.md"
Glob pattern="<category>/<sub>/<proposed-slug>/article.md" path="/Users/rui/Desktop/knowledge-vault"
```

If either matches, report the existing article and ask the user if they want to skip, replace (they must confirm), or save under a different slug.

### Step 3: Fetch content

Use WebFetch (or browser tools if login required) to get the source. Convert to clean markdown. Preserve code blocks, headings, and inline links.

### Step 4: Create the article folder

Path: `/Users/rui/Desktop/knowledge-vault/<category>/<sub>/<slug>/`

**Slug rules:** lowercase, hyphens, no special characters, NEVER named by chapter/lecture number — always by conceptual topic. Example: `transformer-attention-mechanism` not `lecture-03`.

### Step 5: Download assets

For every image in the source:
1. Download to `<category>/<sub>/<slug>/assets/<filename>`
2. Rewrite the markdown reference to Obsidian embed format: `![[assets/<filename>]]`

Skip non-essential decorative images. Preserve diagrams, charts, screenshots that carry information.

### Step 6: Write `article.md` with this exact frontmatter

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

<article body in clean markdown>
```

Rules:
- `compiled: false` — ALWAYS. You do not compile.
- `ingested` — current UTC timestamp in ISO 8601.
- `date` — the source's own publication date, not today.
- `tags` — 2–4 relevant tags based on content.

### Step 7: Report to user

Tell the user:
- Where you saved it: `[[<category>/<sub>/<slug>/article.md]]`
- What you did NOT touch: "Wiki guide and category registry left alone — compile from inside the vault when ready."
- Any judgment calls you made (slug choice, tag choice, category choice).

## Vault Structure Reference

```
knowledge-vault/
  _meta/categories.md         ← READ ONLY (you)
  _templates/                 ← READ ONLY (you)
  wiki/                       ← NEVER TOUCH (you)
  <category>/
    <sub-topic>/
      <article-slug>/         ← YOU CAN CREATE THIS
        article.md            ← YOU WRITE THIS ONCE
        assets/               ← YOU FILL THIS
  <category>/
    <series>/                 ← NOTES — NEVER TOUCH (you)
      <note>.md
```

## Frontmatter Cheat Sheet (the only one you need)

You only ever write Article frontmatter. That's it. Everything else (wiki guides, notes, outputs) is off-limits to you.

## If Something Is Unclear

Don't guess. Ask the user, or open the canonical source: `/Users/rui/Desktop/knowledge-vault/CLAUDE.md`. It's fine to read it when user hits an edge case this skill doesn't cover — but for routine ingest-and-query, everything you need is already here.

## Common Mistakes to Avoid

- Naming a slug by lecture/chapter number instead of topic (user has corrected this before — always conceptual naming).
- Silently creating a new category because no existing one fit — ask first.
- Updating the wiki guide because it "made sense to" — hard no, that's inside-only territory.
- Marking `compiled: true` because you added the content — no, `compiled: false` always.
- Overwriting an existing `article.md` during a "re-ingest" — articles are immutable; save under a new slug or ask the user.
- Forgetting to download images and leaving `https://` refs in the article body — always localize to `![[assets/...]]`.
