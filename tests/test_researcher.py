import pytest
from server.agents.researcher import RESEARCHER_SYSTEM_PROMPT, build_research_prompt


def test_researcher_system_prompt_contains_key_instructions():
    assert "_index.md" in RESEARCHER_SYSTEM_PROMPT
    assert "vault" in RESEARCHER_SYSTEM_PROMPT.lower()
    assert "web search" in RESEARCHER_SYSTEM_PROMPT.lower()


def test_build_research_prompt():
    prompt = build_research_prompt(
        question="What are MCP servers?",
        vault_path="/tmp/vault",
    )
    assert "What are MCP servers?" in prompt
    assert "/tmp/vault" in prompt


def test_build_research_prompt_with_file_context():
    prompt = build_research_prompt(
        question="Tell me more about this",
        vault_path="/tmp/vault",
        file_context="wiki/concepts/mcp.md",
    )
    assert "wiki/concepts/mcp.md" in prompt
