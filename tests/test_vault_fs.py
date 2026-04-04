import json
import pytest
from pathlib import Path
from server.services.vault_fs import (
    read_file,
    write_raw_file,
    list_tree,
    parse_frontmatter,
    update_frontmatter_field,
    get_uncompiled_raw_files,
)


@pytest.fixture
def tmp_vault(tmp_path):
    """Create a temporary vault structure."""
    raw = tmp_path / "raw" / "assets"
    raw.mkdir(parents=True)
    wiki = tmp_path / "wiki" / "concepts"
    wiki.mkdir(parents=True)
    (tmp_path / "wiki" / "_index.md").write_text("# Index\n")
    (tmp_path / "wiki" / "_graph.json").write_text('{"nodes":[],"edges":[]}')
    (tmp_path / "wiki" / "_compiled.json").write_text('{"compiled":{}}')
    return tmp_path


def test_write_and_read_raw_file(tmp_vault):
    path = write_raw_file(
        vault_path=tmp_vault,
        title="Test Article",
        source="https://example.com",
        platform="generic",
        author="Author",
        content="# Hello\n\nSome content.",
    )
    assert path.exists()
    assert path.parent == tmp_vault / "raw"

    frontmatter, body = parse_frontmatter(path)
    assert frontmatter["title"] == "Test Article"
    assert frontmatter["platform"] == "generic"
    assert frontmatter["compiled"] is False
    assert "# Hello" in body


def test_read_file(tmp_vault):
    (tmp_vault / "raw" / "test.md").write_text("---\ntitle: Hi\n---\nBody")
    content = read_file(tmp_vault, "raw/test.md")
    assert "Body" in content


def test_read_file_not_found(tmp_vault):
    with pytest.raises(FileNotFoundError):
        read_file(tmp_vault, "raw/nonexistent.md")


def test_list_tree(tmp_vault):
    (tmp_vault / "raw" / "a.md").write_text("---\ntitle: A\n---\nA")
    (tmp_vault / "raw" / "b.md").write_text("---\ntitle: B\n---\nB")
    (tmp_vault / "wiki" / "concepts" / "c.md").write_text("---\ntitle: C\n---\nC")

    tree = list_tree(tmp_vault)
    assert "raw" in tree
    assert "wiki" in tree
    raw_names = [n["name"] for n in tree["raw"]]
    assert "a.md" in raw_names
    assert "b.md" in raw_names


def test_get_uncompiled_raw_files(tmp_vault):
    (tmp_vault / "raw" / "done.md").write_text(
        "---\ntitle: Done\ncompiled: true\n---\nDone"
    )
    (tmp_vault / "raw" / "new.md").write_text(
        "---\ntitle: New\ncompiled: false\n---\nNew"
    )
    uncompiled = get_uncompiled_raw_files(tmp_vault)
    names = [p.name for p in uncompiled]
    assert "new.md" in names
    assert "done.md" not in names


def test_update_frontmatter_field(tmp_vault):
    p = tmp_vault / "raw" / "edit.md"
    p.write_text("---\ntitle: Edit\ncompiled: false\n---\nBody")
    update_frontmatter_field(p, "compiled", True)
    fm, _ = parse_frontmatter(p)
    assert fm["compiled"] is True
