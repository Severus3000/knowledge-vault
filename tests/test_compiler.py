import pytest
from server.agents.compiler import COMPILER_SYSTEM_PROMPT, build_compile_prompt


def test_compiler_system_prompt_contains_key_instructions():
    assert "wiki/" in COMPILER_SYSTEM_PROMPT
    assert "_index.md" in COMPILER_SYSTEM_PROMPT
    assert "_graph.json" in COMPILER_SYSTEM_PROMPT
    assert "incremental" in COMPILER_SYSTEM_PROMPT.lower()


def test_build_compile_prompt_with_files():
    prompt = build_compile_prompt(
        uncompiled_files=["raw/2026-04-04-test.md"],
        vault_path="/tmp/vault",
    )
    assert "raw/2026-04-04-test.md" in prompt
    assert "/tmp/vault" in prompt


def test_build_compile_prompt_no_files():
    prompt = build_compile_prompt(
        uncompiled_files=[],
        vault_path="/tmp/vault",
    )
    assert "nothing to compile" in prompt.lower()
