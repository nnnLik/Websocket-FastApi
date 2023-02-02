from typing import List

from fastapi import (
    WebSocket,
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        await websocket.close(code=1000, reason=None)

    async def send_answer(self, message: str, websocket: WebSocket):
        await websocket.send_json(message)


manager = ConnectionManager()
