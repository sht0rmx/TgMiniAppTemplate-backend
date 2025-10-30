
from app.middleware.auth import websocket_auth
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.api.routes.ws.manager import bot_websocket


router = APIRouter(prefix="/botupdates", tags=["bot-ws"])

@router.websocket("/ws")
async def bot_ws(ws: WebSocket):
    try:
        await websocket_auth(ws)
        await bot_websocket.connect(ws)

        while True:
            await ws.receive_text()
            print("Data recieved from bot!")

    except WebSocketDisconnect:
        bot_websocket.disconnect()