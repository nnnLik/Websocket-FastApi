from typing import List, Dict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from connection_manager import manager

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/signsense",
    tags=["main"]
)


@router.websocket('/video')
async def video(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive()
            if data['type'] != 'websocket.disconnect':
                print(f'data received {data}')
                await manager.send_answer(f'data -> {data}', websocket)
            else:
                await manager.disconnect(websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print('Disconnected')


@router.get('/', response_class=HTMLResponse)
async def video(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
