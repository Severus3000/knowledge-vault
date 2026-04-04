import json
import pytest
from pathlib import Path
from server.services.index import search_vault, get_stats, get_graph, update_graph


@pytest.fixture
def tmp_vault(tmp_path):
    raw = tmp_path / "raw"
    raw.mkdir()
    wiki = tmp_path / "wiki" / "concepts"
    wiki.mkdir(parents=True)
    (tmp_path / "wiki" / "_index.md").write_text(
        "# Index\nTotal sources: 2 | Articles: 1 | Topics: 1\n"
    )
    (tmp_path / "wiki" / "_graph.json").write_text(
        json.dumps({"nodes": [{"id": "concepts/ai.md", "label": "AI"}], "edges": []})
    )
    (tmp_path / "wiki" / "_compiled.json").write_text('{"compiled":{}}')
    # Add some searchable files
    (tmp_path / "raw" / "article.md").write_text(
        "---\ntitle: MCP Protocol\ncompiled: true\n---\nPlaywright is a browser automation tool."
    )
    (tmp_path / "wiki" / "concepts" / "ai.md").write_text(
        "---\ntitle: AI Agents\ntype: concept\ntags: [ai, agents]\n---\n# AI Agents\nLLMs can do things."
    )
    return tmp_path


def test_search_vault_by_keyword(tmp_vault):
    results = search_vault(tmp_vault, "Playwright")
    assert len(results) >= 1
    assert any("article.md" in r["path"] for r in results)


def test_search_vault_no_results(tmp_vault):
    results = search_vault(tmp_vault, "nonexistent-term-xyz")
    assert len(results) == 0


def test_get_stats(tmp_vault):
    stats = get_stats(tmp_vault)
    assert stats["raw_count"] == 1
    assert stats["wiki_count"] == 1
    assert isinstance(stats["last_compiled"], str)


def test_get_graph(tmp_vault):
    graph = get_graph(tmp_vault)
    assert "nodes" in graph
    assert len(graph["nodes"]) == 1
    assert graph["nodes"][0]["label"] == "AI"


def test_update_graph(tmp_vault):
    update_graph(
        tmp_vault,
        nodes=[
            {"id": "concepts/ai.md", "label": "AI"},
            {"id": "concepts/mcp.md", "label": "MCP"},
        ],
        edges=[{"source": "concepts/ai.md", "target": "concepts/mcp.md"}],
    )
    graph = get_graph(tmp_vault)
    assert len(graph["nodes"]) == 2
    assert len(graph["edges"]) == 1
