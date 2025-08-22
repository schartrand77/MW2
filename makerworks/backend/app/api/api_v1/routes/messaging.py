from __future__ import annotations

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session

from ....db import get_db
from ....audit import log_event

router = APIRouter()

connections: dict[str, WebSocket] = {}


@router.websocket("/ws/dm/{user_id}")
async def websocket_dm(
    websocket: WebSocket, user_id: str, db: Session = Depends(get_db)
):
    await websocket.accept()
    connections[user_id] = websocket
    try:
        while True:
            data = await websocket.receive_json()
            to = data.get("to")
            message = data.get("message")
            target = connections.get(to)
            if target:
                await target.send_json({"from": user_id, "message": message})
            log_event(db, user_id, "dm", {"to": to})
    except WebSocketDisconnect:
        connections.pop(user_id, None)
