import json
import os
import uuid
from app.services.auth.AuthService import AuthUtils
from app.shemes.login_models import WebAppLoginRequest, User
from app.utils import parse_expire
from fastapi import APIRouter, Header, Request
from urllib.parse import parse_qs
from fastapi.responses import JSONResponse

from app.database.database import db_client
from pydantic import ValidationError

router = APIRouter(prefix="/login", tags=["login"])


@router.post("/webapp")
async def webapp_login(request_data: WebAppLoginRequest, request: Request):
    parsed = {k: v[0] for k, v in parse_qs(request_data.initData).items()}
    
    try:
        user_data = User(**json.loads(parsed["user"]))
    except ValidationError:
        return JSONResponse({"detail": "InitData havent right format"}, status_code=401)
    
    if not AuthUtils.check_initdata(initdata=request_data.initData, hash_str=parsed["hash"]):
        return JSONResponse({"detail": "InitData validation failed"}, status_code=401)
    
    user = await db_client.update_user(
        telegram_id=user_data.id, 
        username=user_data.username, 
        name=f"{user_data.first_name} {user_data.last_name}",
        avatar_url=user_data.photo_url)
        
    
    fingerprint = request.headers.get("fingerprint", "default")
    ip = request.client.host if request.client else "127.0.0.1"
    refresh_token = uuid.uuid4()
    
    session = await db_client.update_refresh_session(
        refresh_token=refresh_token, 
        fingerprint=fingerprint, 
        ip=ip,
        user_id=str(user.id))
    
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

    
    access_token = AuthUtils.gen_jwt_token(user_id=user.id, session_id=session.id)
    resp = JSONResponse(content={"access_token": access_token, "user": user_entity}, status_code=200)
    
    resp.set_cookie(
        key="refresh_token",
        value=str(refresh_token),
        httponly=True,
        max_age=int(parse_expire(os.getenv("REFRESH_EXPIRE", "60d")).total_seconds()),
        secure=True,
        samesite="lax" 
    )
    
    return resp