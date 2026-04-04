"""Ingestion API routes."""

from fastapi import APIRouter
from pydantic import BaseModel
from server.agents.ingester import ingest_raw_content


class IngestRequest(BaseModel):
    title: str
    source: str
    platform: str = "generic"
    author: str = ""
    content: str
    date: str | None = None


def init_router(vault_path):
    router = APIRouter(prefix="/api")

    @router.post("/ingest")
    async def ingest(req: IngestRequest):
        path = ingest_raw_content(
            vault_path=vault_path,
            title=req.title,
            source=req.source,
            platform=req.platform,
            author=req.author,
            content=req.content,
            date=req.date,
        )
        rel_path = path.relative_to(vault_path)
        return {"path": str(rel_path), "title": req.title}

    return router
