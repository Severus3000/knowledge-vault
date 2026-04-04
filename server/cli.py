"""CLI interface for the knowledge vault."""

import json
from pathlib import Path

import click

from server.services.vault_fs import read_file
from server.services.index import search_vault, get_stats


@click.group()
@click.option("--vault", default="./vault", help="Path to vault directory")
@click.pass_context
def cli(ctx, vault):
    ctx.ensure_object(dict)
    ctx.obj["vault_path"] = Path(vault).resolve()


@cli.command()
@click.pass_context
def status(ctx):
    """Show vault statistics."""
    stats = get_stats(ctx.obj["vault_path"])
    click.echo(f"Raw sources: {stats['raw_count']}")
    click.echo(f"Wiki articles: {stats['wiki_count']}")
    click.echo(f"Last compiled: {stats['last_compiled']}")


@cli.command()
@click.argument("query")
@click.pass_context
def search(ctx, query):
    """Search the vault for a keyword."""
    results = search_vault(ctx.obj["vault_path"], query)
    if not results:
        click.echo("No results found.")
        return
    for r in results:
        click.echo(f"  {r['title']} ({r['path']})")
        if r["snippet"]:
            click.echo(f"    {r['snippet'][:120]}")


@cli.command()
@click.argument("path")
@click.pass_context
def read(ctx, path):
    """Read a file from the vault."""
    try:
        content = read_file(ctx.obj["vault_path"], path)
        click.echo(content)
    except FileNotFoundError:
        click.echo(f"File not found: {path}")


@cli.command()
@click.argument("question")
@click.pass_context
def ask(ctx, question):
    """Ask a question against the vault (requires ANTHROPIC_API_KEY)."""
    import asyncio
    from server.agents.researcher import run_researcher

    async def _ask():
        async for chunk in run_researcher(
            question=question,
            vault_path=ctx.obj["vault_path"],
        ):
            if chunk["type"] == "text":
                click.echo(chunk["content"], nl=False)
            elif chunk["type"] == "result":
                click.echo(f"\n{chunk['content']}")
        click.echo()

    asyncio.run(_ask())


@cli.command()
@click.argument("title")
@click.argument("source")
@click.option("--platform", default="generic")
@click.option("--author", default="")
@click.option("--content", prompt=True, help="Markdown content (or pipe from stdin)")
@click.pass_context
def ingest(ctx, title, source, platform, author, content):
    """Ingest content into raw/."""
    from server.agents.ingester import ingest_raw_content

    path = ingest_raw_content(
        vault_path=ctx.obj["vault_path"],
        title=title,
        source=source,
        platform=platform,
        author=author,
        content=content,
    )
    click.echo(f"Saved to: {path.relative_to(ctx.obj['vault_path'])}")
