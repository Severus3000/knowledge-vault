"""WebSocket chat endpoint with agent routing."""

import json
import re
from pathlib import Path

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

URL_PATTERN = re.compile(r"https?://\S+")

_sessions: dict[str, str] = {}  # connection_id -> agent session_id


def detect_intent(message: str) -> str:
    """Detect whether the message is a URL, command, or question."""
    stripped = message.strip()
    if URL_PATTERN.match(stripped):
        return "ingest"
    if stripped.lower() in ("compile", "compile the vault", "compile vault"):
        return "compile"
    if stripped.lower() in ("health check", "lint", "check health"):
        return "lint"
    return "research"


def init_router(vault_path: Path) -> APIRouter:
    router = APIRouter()

    @router.websocket("/api/chat")
    async def chat_ws(ws: WebSocket):
        await ws.accept()
        connection_id = str(id(ws))
        try:
            while True:
                data = await ws.receive_text()
                msg = json.loads(data)
                user_text = msg.get("message", "")
                file_context = msg.get("file_context")

                intent = detect_intent(user_text)

                if intent == "ingest":
                    await ws.send_text(json.dumps({
                        "type": "text",
                        "content": f"URL detected: {user_text.strip()}\nTo ingest this URL, use Claude Code with the web-access skill:\n\n```\nvault ingest \"Title\" \"{user_text.strip()}\" --content \"<extracted content>\"\n```\n\nOr use the `vault_ingest` MCP tool in Claude Code — web-access will fetch and extract the content automatically.",
                    }))
                    await ws.send_text(json.dumps({"type": "done"}))

                elif intent == "compile":
                    await ws.send_text(json.dumps({
                        "type": "text",
                        "content": "Starting vault compilation...",
                    }))
                    from server.agents.compiler import run_compiler
                    result = await run_compiler(vault_path)
                    await ws.send_text(json.dumps({
                        "type": "text",
                        "content": result,
                    }))
                    await ws.send_text(json.dumps({"type": "done"}))

                elif intent == "research":
                    from server.agents.researcher import run_researcher
                    session_id = _sessions.get(connection_id)
                    async for chunk in run_researcher(
                        question=user_text,
                        vault_path=vault_path,
                        session_id=session_id,
                        file_context=file_context,
                    ):
                        if chunk["type"] == "session":
                            _sessions[connection_id] = chunk["session_id"]
                        await ws.send_text(json.dumps(chunk))
                    await ws.send_text(json.dumps({"type": "done"}))

                else:
                    await ws.send_text(json.dumps({
                        "type": "text",
                        "content": "Linter agent is not yet implemented.",
                    }))
                    await ws.send_text(json.dumps({"type": "done"}))

        except WebSocketDisconnect:
            _sessions.pop(connection_id, None)

    return router
