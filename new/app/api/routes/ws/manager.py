from fastapi import WebSocket

class WSNotFound(Exception):
    pass

class WSManager:
    def __init__(self):
        self.ws: WebSocket | None = None

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.ws = ws

    def disconnect(self):
        self.ws = None

    async def send_json(self, message: dict):
        if self.ws:
            await self.ws.send_json(message)
        else:
            raise WSNotFound()

bot_websocket = WSManager()
