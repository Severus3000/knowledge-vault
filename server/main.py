"""FastAPI application entry point."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.config import VAULT_PATH
from server.api.vault import init_router as init_vault
from server.api.ingest import init_router as init_ingest


def create_app(vault_path: Path | None = None) -> FastAPI:
    vp = vault_path or VAULT_PATH
    app = FastAPI(title="Knowledge Vault", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://localhost:3000"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(init_vault(vp))
    app.include_router(init_ingest(vp))

    return app


# Default app instance for `uvicorn server.main:app`
app = create_app()
