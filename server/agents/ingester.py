"""Ingester Agent — saves content to raw/.

Content fetching is handled externally by the web-access Claude Code skill
(https://github.com/eze-is/web-access), which extracts content from any
platform via CDP/WebFetch/Jina. This module accepts pre-fetched content.
"""

from pathlib import Path

from server.services.vault_fs import write_raw_file


def ingest_raw_content(
    vault_path: Path,
    title: str,
    source: str,
    platform: str,
    author: str,
    content: str,
    date: str | None = None,
) -> Path:
    """Ingest pre-fetched content into raw/. Returns the saved file path.

    Content fetching is handled by the web-access Claude Code skill.
    Workflow: URL → web-access extracts content → this function saves to raw/.
    """
    return write_raw_file(
        vault_path=vault_path,
        title=title,
        source=source,
        platform=platform,
        author=author,
        content=content,
        date=date,
    )
