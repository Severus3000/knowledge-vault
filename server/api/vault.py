"""Vault REST API routes."""

from fastapi import APIRouter, HTTPException, Query
from server.services.vault_fs import read_file, list_tree, parse_frontmatter
from server.services.index import search_vault, get_stats, get_graph


def init_router(vault_path):
    router = APIRouter(prefix="/api/vault")

    @router.get("/tree")
    async def get_tree():
        return list_tree(vault_path)

    @router.get("/read")
    async def read(path: str = Query(...)):
        try:
            content = read_file(vault_path, path)
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="File not found")
        full_path = vault_path / path
        try:
            fm, body = parse_frontmatter(full_path)
            return {"content": content, "frontmatter": fm, "body": body}
        except Exception:
            return {"content": content, "frontmatter": {}, "body": content}

    @router.get("/search")
    async def search(q: str = Query(...)):
        results = search_vault(vault_path, q)
        return {"results": results}

    @router.get("/stats")
    async def stats():
        return get_stats(vault_path)

    @router.get("/graph")
    async def graph():
        return get_graph(vault_path)

    return router
