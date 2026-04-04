import json
import pytest
from pathlib import Path
from click.testing import CliRunner
from server.cli import cli


@pytest.fixture
def tmp_vault(tmp_path):
    (tmp_path / "raw" / "assets").mkdir(parents=True)
    wiki = tmp_path / "wiki" / "concepts"
    wiki.mkdir(parents=True)
    (tmp_path / "wiki" / "_index.md").write_text("# Index\nLast compiled: never\nTotal sources: 1 | Articles: 1 | Topics: 0\n")
    (tmp_path / "wiki" / "_graph.json").write_text('{"nodes":[],"edges":[]}')
    (tmp_path / "wiki" / "_compiled.json").write_text('{"compiled":{}}')
    (tmp_path / "raw" / "test.md").write_text("---\ntitle: Test MCP\ncompiled: false\n---\n# MCP\nPlaywright automation")
    (tmp_path / "wiki" / "concepts" / "ai.md").write_text("---\ntitle: AI\ntype: concept\n---\n# AI\nAgent article")
    return tmp_path


def test_status(tmp_vault):
    runner = CliRunner()
    result = runner.invoke(cli, ["--vault", str(tmp_vault), "status"])
    assert result.exit_code == 0
    assert "1" in result.output


def test_search(tmp_vault):
    runner = CliRunner()
    result = runner.invoke(cli, ["--vault", str(tmp_vault), "search", "MCP"])
    assert result.exit_code == 0
    assert "Test MCP" in result.output or "test.md" in result.output


def test_search_no_results(tmp_vault):
    runner = CliRunner()
    result = runner.invoke(cli, ["--vault", str(tmp_vault), "search", "zzzznonexistent"])
    assert result.exit_code == 0
    assert "No results" in result.output


def test_read(tmp_vault):
    runner = CliRunner()
    result = runner.invoke(cli, ["--vault", str(tmp_vault), "read", "raw/test.md"])
    assert result.exit_code == 0
    assert "# MCP" in result.output


def test_read_not_found(tmp_vault):
    runner = CliRunner()
    result = runner.invoke(cli, ["--vault", str(tmp_vault), "read", "raw/nope.md"])
    assert result.exit_code == 0
    assert "not found" in result.output.lower()
