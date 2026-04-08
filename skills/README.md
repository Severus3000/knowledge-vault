# Skills

These two Claude Code skills are required for the vault to operate end-to-end. Both are vendored here so the system is self-contained — clone the repo and install them in one step.

## What each skill does

| Skill | Purpose | Origin |
|---|---|---|
| [`knowledge-vault/`](./knowledge-vault/) | Teaches Claude how to ingest into and query this vault from **any** working directory. Read-mostly with one safe write (a new article folder). | Self-authored |
| [`web-access/`](./web-access/) | Browser-based fetching for ingestion — handles login walls, JS-rendered pages, and platforms that block static scrapers (Xiaohongshu, WeChat, etc.). Used during the **Ingest** workflow. | Third-party, MIT — by [一泽 Eze](https://github.com/eze-is) ([upstream repo](https://github.com/eze-is/web-access)) |

## Install

Claude Code discovers skills under `~/.claude/skills/`. Symlink (recommended — picks up edits automatically) or copy:

```bash
# from the repo root
ln -s "$PWD/skills/knowledge-vault" ~/.claude/skills/knowledge-vault
ln -s "$PWD/skills/web-access"      ~/.claude/skills/web-access
```

Or copy if you prefer a static install:

```bash
cp -R skills/knowledge-vault ~/.claude/skills/
cp -R skills/web-access      ~/.claude/skills/
```

Restart Claude Code (or open a new session) so the skills are picked up.

## web-access prerequisites

The `web-access` skill drives a real Chrome via the Chrome DevTools Protocol. One-time setup:

1. **Node.js 22+** (for native WebSocket).
2. In Chrome, open `chrome://inspect/#remote-debugging` and check **"Allow remote debugging for this browser instance"**. Restart Chrome if prompted.
3. First run will start a local CDP proxy automatically (`scripts/cdp-proxy.mjs`).

Verify with:

```bash
node ~/.claude/skills/web-access/scripts/check-deps.mjs
```

## Updating web-access from upstream

`web-access` is a vendored snapshot. To pull a newer version:

```bash
cd /tmp && git clone https://github.com/eze-is/web-access.git
rsync -a --delete --exclude='.git' /tmp/web-access/ \
  /Users/rui/Desktop/knowledge-vault/skills/web-access/
```

Then commit the diff. The `knowledge-vault` skill is maintained in this repo directly — edit `skills/knowledge-vault/SKILL.md` here.

## License

- `knowledge-vault/` — MIT (same as the rest of this repo).
- `web-access/` — MIT, © 一泽 Eze. See the [upstream README](./web-access/README.md) for full attribution.
