from fastapi import APIRouter

from app.api.routes.auth import main as auth
from app.api.routes import sessions as sessions
from app.api.routes.ws import websocket
from fastapi.responses import JSONResponse

api_router = APIRouter()

api_router.include_router(auth.sub_router)
api_router.include_router(sessions.router)
api_router.include_router(websocket.router)

@api_router.get("/ping", tags=["ping"])
def ping_pong():
    return JSONResponse({"detail": "pong"}, status_code=200)