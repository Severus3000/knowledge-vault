"""MCP server exposing vault tools to Claude Code."""

import asyncio
import json
import os
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from server.services.vault_fs import read_file
from server.services.index import search_vault, get_stats, get_graph

VAULT_PATH = Path(os.environ.get("VAULT_PATH", "./vault")).resolve()

server = Server("knowledge-vault")


@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="vault_search",
            description="Search the knowledge vault for articles matching a keyword",
            inputSchema={
                "type": "object",
                "properties": {"query": {"type": "string", "description": "Search keyword"}},
                "required": ["query"],
            },
        ),
        Tool(
            name="vault_read",
            description="Read a specific article from the vault by relative path",
            inputSchema={
                "type": "object",
                "properties": {"path": {"type": "string", "description": "Relative path, e.g. wiki/concepts/ai.md"}},
                "required": ["path"],
            },
        ),
        Tool(
            name="vault_index",
            description="Get the master index summary of the knowledge vault",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="vault_status",
            description="Get vault statistics (article counts, last compiled time)",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="vault_ingest",
            description="Ingest pre-fetched content into the vault raw/ directory",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "source": {"type": "string", "description": "Source URL"},
                    "platform": {"type": "string", "default": "generic"},
                    "author": {"type": "string", "default": ""},
                    "content": {"type": "string", "description": "Markdown content"},
                },
                "required": ["title", "source", "content"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "vault_search":
        results = search_vault(VAULT_PATH, arguments["query"])
        return [TextContent(type="text", text=json.dumps(results, indent=2, ensure_ascii=False))]

    elif name == "vault_read":
        try:
            content = read_file(VAULT_PATH, arguments["path"])
            return [TextContent(type="text", text=content)]
        except FileNotFoundError:
            return [TextContent(type="text", text=f"File not found: {arguments['path']}")]

    elif name == "vault_index":
        try:
            content = read_file(VAULT_PATH, "wiki/_index.md")
            return [TextContent(type="text", text=content)]
        except FileNotFoundError:
            return [TextContent(type="text", text="No index file found. Run compilation first.")]

    elif name == "vault_status":
        stats = get_stats(VAULT_PATH)
        return [TextContent(type="text", text=json.dumps(stats, indent=2))]

    elif name == "vault_ingest":
        from server.agents.ingester import ingest_raw_content
        path = ingest_raw_content(
            vault_path=VAULT_PATH,
            title=arguments["title"],
            source=arguments["source"],
            platform=arguments.get("platform", "generic"),
            author=arguments.get("author", ""),
            content=arguments["content"],
        )
        rel = path.relative_to(VAULT_PATH)
        return [TextContent(type="text", text=f"Ingested to: {rel}")]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)


if __name__ == "__main__":
    asyncio.run(main())
