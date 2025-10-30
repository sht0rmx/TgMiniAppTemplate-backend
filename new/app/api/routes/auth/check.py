from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from app.middleware.auth import require_auth
from app.database.database import NotFound, db_client

router = APIRouter(tags=["check"])

@router.get("/check", dependencies=[Depends(require_auth)])
async def check(request: Request):
    try:
        user = await db_client.get_user(uid=request.state.user_id)
        
        user_entity = {
            "id": str(user.id),
            "telegram_id": user.telegram_id,
            "username": user.username,
            "name": user.name,
            "role": user.role,
            "avatar_url": user.avatar_url,
            "last_seen": user.last_seen.isoformat(),
            "created_at": user.created_at.isoformat()
        }
        
        JSONResponse({"user": user_entity}, status_code=200)
    except NotFound:
        JSONResponse({"detail": "user not found"}, status_code=406)

