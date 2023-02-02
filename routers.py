from datetime import datetime
from typing import List, Dict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from connection_manager import manager
from service.test import heavy_data_processing

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/signsense",
    tags=["main"]
)


@router.websocket('/video')
async def video(websocket: WebSocket):
    await manager.connect(websocket)
    while True:
        try:
            data = await websocket.receive_json()
            message_processed = await heavy_data_processing(data)
            await websocket.send_json(
                {
                    "message": message_processed,
                    "time": datetime.now().strftime("%H:%M:%S"),
                }
            )
        except WebSocketDisconnect:
            break
    # try:
    #     while True:
    #         data = await websocket.receive()
    #         if data['type'] != 'websocket.disconnect':
    #             print(f'data received {data}')
    #             await manager.send_answer(f'data -> {data}', websocket)
    #         else:
    #             await manager.disconnect(websocket)
    # except WebSocketDisconnect:
    #     # manager.disconnect(websocket)
    #     print('Disconnected')
    #     break


@router.get('/', response_class=HTMLResponse)
async def video(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
