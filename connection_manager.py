from typing import List

from fastapi import (
    Cookie,
    Depends,
    Query,
    WebSocket,
    WebSocketException,
    WebSocketDisconnect,
    status,
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
        # for connection in self.active_connections:
        #     await connection.send_json(message)
        await websocket.send_json(message)


manager = ConnectionManager()
