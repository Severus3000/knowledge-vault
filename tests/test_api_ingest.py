import pytest
from httpx import AsyncClient, ASGITransport
from server.main import create_app


@pytest.fixture
def tmp_vault(tmp_path):
    (tmp_path / "raw" / "assets").mkdir(parents=True)
    (tmp_path / "wiki").mkdir()
    (tmp_path / "wiki" / "_index.md").write_text("# Index\n")
    (tmp_path / "wiki" / "_graph.json").write_text('{"nodes":[],"edges":[]}')
    (tmp_path / "wiki" / "_compiled.json").write_text('{"compiled":{}}')
    return tmp_path


@pytest.fixture
def app(tmp_vault):
    return create_app(vault_path=tmp_vault)


@pytest.mark.asyncio
async def test_ingest_content(app, tmp_vault):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/api/ingest", json={
            "title": "New Article",
            "source": "https://example.com",
            "platform": "generic",
            "author": "Test",
            "content": "# Hello\nWorld",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["path"].startswith("raw/")
        assert (tmp_vault / data["path"]).exists()
