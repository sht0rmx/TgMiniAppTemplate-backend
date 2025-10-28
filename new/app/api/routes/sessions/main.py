from app.api.routes.sessions import all_sessions, current
from fastapi import APIRouter


sub_router = APIRouter(prefix="/sessions", tags=["Sessions"])

sub_router.include_router(all_sessions.router)
sub_router.include_router(current.router)