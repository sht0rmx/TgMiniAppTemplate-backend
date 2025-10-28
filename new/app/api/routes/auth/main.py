from app.api.routes.auth import check, login, token
from fastapi import APIRouter


sub_router = APIRouter(prefix="/auth", tags=["Auth"])

sub_router.include_router(login.router)
sub_router.include_router(check.router)
sub_router.include_router(token.router)