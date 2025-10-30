from fastapi import APIRouter

from app.api.routes.auth import main as auth
from app.api.routes.sessions import main as sessions
from app.api.routes.ws import websocket
from fastapi.responses import JSONResponse

api_router = APIRouter()

api_router.include_router(auth.sub_router)
api_router.include_router(sessions.sub_router)
api_router.include_router(websocket.router)

@api_router.get("/ping", tags=["ping"])
def ping_pong():
    return JSONResponse({"detail": "pong"}, status_code=200)