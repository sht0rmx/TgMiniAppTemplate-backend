from fastapi import APIRouter

from app.api.routes.auth import main as auth
from app.api.routes.sessions import main as sessions
from app.api.routes import bot_updates, ping

api_router = APIRouter()

api_router.include_router(auth.sub_router)
api_router.include_router(sessions.sub_router)
api_router.include_router(bot_updates.router)
api_router.include_router(ping.router)