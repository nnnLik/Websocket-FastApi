from typing import List

from fastapi import APIRouter

from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from fastapi import (
    Cookie,
    Depends,
    Query,
    WebSocket,
    WebSocketException,
    WebSocketDisconnect,
    status,
)

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/signsense",
    tags=["main"]
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_answer(self, message: str):
        ...


manager = ConnectionManager()


@router.websocket('/video')
async def video(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            frame = await websocket.receive()
            print('frame received')
            await manager.send_answer('hi')
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print('Disconnected')
        await manager.send_answer('Disconnected')


@router.get('/', response_class=HTMLResponse)
async def video(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
