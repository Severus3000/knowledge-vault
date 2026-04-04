"""Compiler Agent — turns raw content into structured wiki articles."""

import asyncio
from pathlib import Path

from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage

COMPILER_SYSTEM_PROMPT = """\
You are the Compiler Agent for a personal knowledge vault.

Your job: read new raw files and incrementally compile them into a structured wiki.

## Vault Layout
- raw/ — original ingested content (markdown with frontmatter)
- wiki/ — AI-compiled knowledge articles (you write and maintain these)
  - wiki/_index.md — master index with topics, recent additions, article summaries
  - wiki/_graph.json — knowledge graph {"nodes": [...], "edges": [...]}
  - wiki/_compiled.json — tracks which raw files have been compiled
  - wiki/concepts/ — concept articles synthesizing knowledge across sources
  - wiki/summaries/ — per-source summaries
  - wiki/topics/ — topic cluster directories

## Your Process
1. Read each uncompiled raw file
2. Read wiki/_index.md to understand existing structure
3. For each raw file, decide:
   - Does it introduce a new concept? → Create wiki/concepts/<slug>.md
   - Does it relate to an existing concept? → Edit that article, add info + backlink
   - Does it suggest a new topic cluster? → Create wiki/topics/<name>/
4. Always create a summary in wiki/summaries/<raw-filename>.md
5. Update wiki/_index.md with new entries and updated summaries
6. Update wiki/_graph.json with new nodes and edges
7. After processing each raw file, edit its frontmatter to set compiled: true

## Wiki Article Format
Use this frontmatter:
---
title: "Article Title"
type: concept  # concept | topic | summary
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - raw/source-file.md
related:
  - concepts/related.md
tags: [tag1, tag2]
---

## Rules
- Write in clear, concise prose. Synthesize, don't just copy.
- Always link back to raw sources.
- Cross-link related concepts with [[wiki-links]].
- Be incremental — only process what's new, don't rewrite existing articles unnecessarily.
- Keep _index.md Article Summaries section updated with one-paragraph summaries.
"""


def build_compile_prompt(uncompiled_files: list[str], vault_path: str) -> str:
    """Build the prompt for a compilation run."""
    if not uncompiled_files:
        return "There is nothing to compile. All raw files are already compiled."

    file_list = "\n".join(f"- {f}" for f in uncompiled_files)
    return f"""\
Working directory: {vault_path}

The following raw files need to be compiled into the wiki:

{file_list}

Read each file, then compile them into the wiki following your instructions.
After processing each file, update its frontmatter to set `compiled: true`.
Finally, update _index.md and _graph.json.
"""


async def run_compiler(vault_path: Path) -> str:
    """Run the compiler agent. Returns a summary of what was compiled."""
    from server.services.vault_fs import get_uncompiled_raw_files

    uncompiled = get_uncompiled_raw_files(vault_path)
    file_names = [str(p.relative_to(vault_path)) for p in uncompiled]

    prompt = build_compile_prompt(file_names, str(vault_path))
    if not uncompiled:
        return "Nothing to compile."

    result_text = ""
    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            system_prompt=COMPILER_SYSTEM_PROMPT,
            allowed_tools=["Read", "Write", "Edit", "Glob", "Grep"],
            permission_mode="acceptEdits",
            cwd=str(vault_path),
        ),
    ):
        if isinstance(message, ResultMessage):
            result_text = getattr(message, "result", "Compilation complete.")
        elif isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    result_text = block.text

    return result_text or "Compilation complete."
