# Knowledge Vault

Multi-vault personal knowledge base powered by Claude Code and viewed in Obsidian. Raw sources are ingested, compiled into a structured wiki by Claude Code, and operated on for Q&A, research, and output generation.

Inspired by [Karpathy's LLM Knowledge Bases](https://x.com/karpathy/status/1936469592498032744) approach.

## Setup

1. Open this folder as an Obsidian vault
2. Install Obsidian community plugins: **Marp Slides**, **Dataview**
3. Ensure [Claude Code](https://docs.anthropic.com/en/docs/claude-code) is installed with `ANTHROPIC_API_KEY` set
4. For PDF output: install [pandoc](https://pandoc.org/installing.html)

## Usage

Everything is done by prompting Claude Code in this directory:

```
"Create a new vault for quantum computing"
"Ingest https://arxiv.org/abs/... into the quantum-computing vault"
"Compile the quantum-computing vault"
"What do I know about entanglement? Check quantum-computing."
"Create a Marp presentation on quantum gates from the quantum-computing vault"
"Generate a PDF summary of my quantum-computing vault"
```

## Structure

```
knowledge-vault/
├── .obsidian/          # Obsidian config & plugins
├── CLAUDE.md           # Instructions for Claude Code
├── _templates/         # Markdown templates for all file types
├── _meta/
│   └── vaults.md       # Registry of all vaults
├── <vault-name>/       # One per knowledge base
│   ├── raw/            # Ingested sources + assets/
│   ├── wiki/           # Compiled articles (_index.md, summaries/, concepts/)
│   └── outputs/        # Research, slides, charts, PDFs
└── ...more vaults
```

## License

MIT
