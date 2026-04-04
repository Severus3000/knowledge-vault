import pytest
from pathlib import Path
from server.agents.ingester import ingest_raw_content
from server.services.vault_fs import parse_frontmatter


@pytest.fixture
def tmp_vault(tmp_path):
    (tmp_path / "raw" / "assets").mkdir(parents=True)
    (tmp_path / "wiki").mkdir()
    return tmp_path


def test_ingest_raw_content(tmp_vault):
    path = ingest_raw_content(
        vault_path=tmp_vault,
        title="Test Article",
        source="https://example.com",
        platform="generic",
        author="Author",
        content="# Test\n\nThis is test content.",
    )
    assert path.exists()
    fm, body = parse_frontmatter(path)
    assert fm["title"] == "Test Article"
    assert fm["compiled"] is False
    assert "# Test" in body


def test_ingest_raw_content_with_date(tmp_vault):
    path = ingest_raw_content(
        vault_path=tmp_vault,
        title="Dated Article",
        source="https://example.com",
        platform="wechat",
        author="Author",
        content="Content here.",
        date="2026-01-15",
    )
    assert "2026-01-15" in path.name
