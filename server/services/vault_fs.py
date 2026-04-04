"""Filesystem operations for the knowledge vault."""

import re
from datetime import datetime, timezone
from pathlib import Path

import frontmatter


def parse_frontmatter(path: Path) -> tuple[dict, str]:
    """Parse a markdown file into (frontmatter_dict, body_string)."""
    post = frontmatter.load(str(path))
    return dict(post.metadata), post.content


def read_file(vault_path: Path, relative_path: str) -> str:
    """Read a file from the vault by relative path. Returns full content including frontmatter."""
    full_path = vault_path / relative_path
    if not full_path.exists():
        raise FileNotFoundError(f"Not found: {relative_path}")
    return full_path.read_text(encoding="utf-8")


def write_raw_file(
    vault_path: Path,
    title: str,
    source: str,
    platform: str,
    author: str,
    content: str,
    date: str | None = None,
) -> Path:
    """Write a new raw file with frontmatter. Returns the file path."""
    now = datetime.now(timezone.utc)
    date_str = date or now.strftime("%Y-%m-%d")
    slug = re.sub(r"[^\w\s-]", "", title.lower())
    slug = re.sub(r"[\s]+", "-", slug).strip("-")[:60]
    filename = f"{date_str}-{slug}.md"

    post = frontmatter.Post(
        content,
        title=title,
        source=source,
        platform=platform,
        author=author,
        date=date_str,
        ingested=now.isoformat(),
        tags=[],
        compiled=False,
    )

    path = vault_path / "raw" / filename
    path.write_text(frontmatter.dumps(post), encoding="utf-8")
    return path


def list_tree(vault_path: Path) -> dict:
    """List vault directory tree as a dict of {section: [file_entries]}."""
    tree = {}
    for section in ["raw", "wiki", "outputs"]:
        section_path = vault_path / section
        if not section_path.exists():
            tree[section] = []
            continue
        entries = []
        for p in sorted(section_path.rglob("*.md")):
            rel = p.relative_to(vault_path / section)
            entries.append({
                "name": p.name,
                "path": f"{section}/{rel}",
                "dir": str(rel.parent) if str(rel.parent) != "." else "",
            })
        tree[section] = entries
    return tree


def get_uncompiled_raw_files(vault_path: Path) -> list[Path]:
    """Return raw files where compiled: false."""
    raw_dir = vault_path / "raw"
    uncompiled = []
    for p in raw_dir.glob("*.md"):
        try:
            fm, _ = parse_frontmatter(p)
            if fm.get("compiled") is False:
                uncompiled.append(p)
        except Exception:
            continue
    return uncompiled


def update_frontmatter_field(path: Path, field: str, value) -> None:
    """Update a single frontmatter field in a markdown file."""
    post = frontmatter.load(str(path))
    post.metadata[field] = value
    path.write_text(frontmatter.dumps(post), encoding="utf-8")
