# Knowledge Vault

AI-powered personal knowledge base. Throw in links from WeChat, Xiaohongshu, X/Twitter, YouTube, Bilibili — an AI agent organizes them into a structured wiki you can chat with.

Inspired by [Karpathy's LLM Knowledge Bases](https://x.com/karpathy) approach.

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- `ANTHROPIC_API_KEY` set in environment

### Install

```bash
# Backend
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Frontend
cd web && npm install && cd ..
```

### Run

```bash
# Terminal 1: Backend
uvicorn server.main:app --reload --port 8000

# Terminal 2: Frontend
cd web && npm run dev
```

Open http://localhost:5173

### CLI

```bash
vault status                                    # Vault stats
vault search "MCP servers"                      # Search articles
vault read wiki/concepts/ai.md                  # Read an article
vault ask "What do I know about browser automation?"  # AI Q&A
vault ingest "Title" "https://url" --content "# Markdown content"
```

### MCP Server (Claude Code integration)

```bash
claude mcp add knowledge-vault -- python -m server.mcp_server
```

Then in Claude Code: use `vault_search`, `vault_read`, `vault_ask`, `vault_index`, `vault_status`, `vault_ingest` tools.

### Content Ingestion (web-access skill)

Install the [web-access](https://github.com/eze-is/web-access) Claude Code skill for intelligent content extraction:

```bash
git clone https://github.com/eze-is/web-access.git ~/.claude/skills/web-access
```

Then in Claude Code, simply say: "Ingest this article into my vault: https://..." — web-access fetches and extracts the content, then calls `vault_ingest` to save it.

Supports: WeChat articles, XHS posts, YouTube transcripts, Bilibili, blogs, and any web page.

## Architecture

```
knowledge-vault/
├── server/          # Python FastAPI backend
│   ├── agents/      # AI agents (compiler, researcher, ingester)
│   ├── api/         # REST + WebSocket endpoints
│   ├── services/    # Core services (vault_fs, index)
│   ├── cli.py       # Click CLI
│   └── mcp_server.py  # MCP server for Claude Code
├── web/             # React + Vite frontend
│   └── src/
│       ├── components/  # Sidebar, ArticleViewer, ChatPanel, GraphView, StatusBar
│       ├── api.ts       # API helpers
│       └── types.ts     # Shared types
└── vault/           # Knowledge storage (raw/, wiki/, outputs/)
```

## License

MIT
