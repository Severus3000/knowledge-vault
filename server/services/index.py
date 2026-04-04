"""Index, search, and graph operations for the knowledge vault."""

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from server.services.vault_fs import parse_frontmatter


def search_vault(vault_path: Path, query: str) -> list[dict]:
    """Simple keyword search across all markdown files in vault."""
    results = []
    query_lower = query.lower()
    for md_file in vault_path.rglob("*.md"):
        if md_file.name.startswith("_"):
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
        except Exception:
            continue
        if query_lower in content.lower():
            rel = md_file.relative_to(vault_path)
            title = str(rel)
            try:
                fm, _ = parse_frontmatter(md_file)
                title = fm.get("title", title)
            except Exception:
                pass
            snippet = ""
            for line in content.split("\n"):
                if query_lower in line.lower():
                    snippet = line.strip()[:200]
                    break
            results.append({"path": str(rel), "title": title, "snippet": snippet})
    return results


def get_stats(vault_path: Path) -> dict:
    """Get vault statistics."""
    raw_dir = vault_path / "raw"
    wiki_dir = vault_path / "wiki"
    raw_count = len(list(raw_dir.glob("*.md"))) if raw_dir.exists() else 0
    wiki_count = sum(
        1
        for f in wiki_dir.rglob("*.md")
        if not f.name.startswith("_")
    ) if wiki_dir.exists() else 0

    index_file = wiki_dir / "_index.md"
    last_compiled = "never"
    if index_file.exists():
        content = index_file.read_text(encoding="utf-8")
        match = re.search(r"Last compiled: (.+)", content)
        if match:
            last_compiled = match.group(1).strip()

    return {
        "raw_count": raw_count,
        "wiki_count": wiki_count,
        "last_compiled": last_compiled,
    }


def get_graph(vault_path: Path) -> dict:
    """Read the knowledge graph from _graph.json."""
    graph_file = vault_path / "wiki" / "_graph.json"
    if not graph_file.exists():
        return {"nodes": [], "edges": []}
    return json.loads(graph_file.read_text(encoding="utf-8"))


def update_graph(vault_path: Path, nodes: list[dict], edges: list[dict]) -> None:
    """Write the knowledge graph to _graph.json."""
    graph_file = vault_path / "wiki" / "_graph.json"
    graph_file.write_text(
        json.dumps({"nodes": nodes, "edges": edges}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
