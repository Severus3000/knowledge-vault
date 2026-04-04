import json
import pytest
from pathlib import Path
from httpx import AsyncClient, ASGITransport
from server.main import create_app


@pytest.fixture
def tmp_vault(tmp_path):
    (tmp_path / "raw" / "assets").mkdir(parents=True)
    wiki = tmp_path / "wiki" / "concepts"
    wiki.mkdir(parents=True)
    (tmp_path / "wiki" / "_index.md").write_text("# Index\nLast compiled: never\nTotal sources: 1 | Articles: 1 | Topics: 0\n")
    (tmp_path / "wiki" / "_graph.json").write_text('{"nodes":[],"edges":[]}')
    (tmp_path / "wiki" / "_compiled.json").write_text('{"compiled":{}}')
    (tmp_path / "raw" / "test.md").write_text("---\ntitle: Test\ncompiled: false\n---\n# Test\nContent")
    (tmp_path / "wiki" / "concepts" / "ai.md").write_text("---\ntitle: AI\ntype: concept\ntags: [ai]\n---\n# AI\nArticle")
    return tmp_path


@pytest.fixture
def app(tmp_vault):
    return create_app(vault_path=tmp_vault)


@pytest.mark.asyncio
async def test_get_tree(app, tmp_vault):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/vault/tree")
        assert resp.status_code == 200
        data = resp.json()
        assert "raw" in data
        assert "wiki" in data


@pytest.mark.asyncio
async def test_read_file(app, tmp_vault):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/vault/read", params={"path": "raw/test.md"})
        assert resp.status_code == 200
        assert "# Test" in resp.json()["content"]


@pytest.mark.asyncio
async def test_read_file_not_found(app, tmp_vault):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/vault/read", params={"path": "raw/nope.md"})
        assert resp.status_code == 404


@pytest.mark.asyncio
async def test_search(app, tmp_vault):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/vault/search", params={"q": "AI"})
        assert resp.status_code == 200
        assert len(resp.json()["results"]) >= 1


@pytest.mark.asyncio
async def test_stats(app, tmp_vault):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/vault/stats")
        assert resp.status_code == 200
        data = resp.json()
        assert data["raw_count"] == 1


@pytest.mark.asyncio
async def test_graph(app, tmp_vault):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/vault/graph")
        assert resp.status_code == 200
        assert "nodes" in resp.json()
