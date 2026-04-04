"""Researcher Agent — Q&A against the knowledge vault."""

import asyncio
from pathlib import Path
from typing import AsyncIterator

from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AssistantMessage,
    ResultMessage,
    SystemMessage,
)

RESEARCHER_SYSTEM_PROMPT = """\
You are the Researcher Agent for a personal knowledge vault.

Your job: answer questions by searching the vault, synthesizing knowledge, and optionally filing results back.

## Vault Layout
- raw/ — original ingested sources
- wiki/ — compiled knowledge articles
  - wiki/_index.md — master index with article summaries (READ THIS FIRST)
- outputs/ — your generated outputs (research, presentations)

## Your Process
1. ALWAYS start by reading wiki/_index.md to understand what's available
2. Use Grep to search for relevant keywords across the vault
3. Read the most relevant articles in full
4. Synthesize an answer from vault content FIRST
5. Only use web search if the vault doesn't have enough information
6. If your answer produces valuable new knowledge, offer to file it:
   - New concept article → wiki/concepts/
   - Research output → outputs/research/
   - Presentation → outputs/presentations/ (Marp format)

## Rules
- Cite your vault sources: "According to [[concepts/mcp.md]], ..."
- Distinguish between vault knowledge and web search results
- Keep answers focused and well-structured
- When filing back to wiki, follow the wiki article format with proper frontmatter
"""


def build_research_prompt(
    question: str,
    vault_path: str,
    file_context: str | None = None,
) -> str:
    """Build the prompt for a research query."""
    context_line = ""
    if file_context:
        context_line = f"\nThe user is currently viewing: {file_context}\n"

    return f"""\
Working directory: {vault_path}
{context_line}
User question: {question}
"""


async def run_researcher(
    question: str,
    vault_path: Path,
    session_id: str | None = None,
    file_context: str | None = None,
) -> AsyncIterator[dict]:
    """Run the researcher agent, yielding streaming messages.

    Yields dicts with keys:
        - {"type": "text", "content": "..."} for text chunks
        - {"type": "tool", "name": "...", "input": {...}} for tool calls
        - {"type": "result", "content": "..."} for final result
        - {"type": "session", "session_id": "..."} for session tracking
    """
    prompt = build_research_prompt(question, str(vault_path), file_context)

    options = ClaudeAgentOptions(
        system_prompt=RESEARCHER_SYSTEM_PROMPT,
        allowed_tools=["Read", "Glob", "Grep", "Write", "WebSearch", "WebFetch"],
        permission_mode="acceptEdits",
        cwd=str(vault_path),
    )
    if session_id:
        options = ClaudeAgentOptions(resume=session_id)

    async for message in query(prompt=prompt, options=options):
        if isinstance(message, SystemMessage) and message.subtype == "init":
            yield {"type": "session", "session_id": message.data.get("session_id")}
        elif isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    yield {"type": "text", "content": block.text}
                elif hasattr(block, "name"):
                    yield {"type": "tool", "name": block.name}
        elif isinstance(message, ResultMessage):
            yield {"type": "result", "content": getattr(message, "result", "")}
