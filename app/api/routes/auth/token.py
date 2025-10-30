import os
from typing import Union
import uuid
from app.api.routes.ws.manager import WSNotFound, bot_websocket
from app.middleware.auth import require_origin, deny_bot, require_auth
from app.services.auth.AuthService import AuthUtils
from app.shemes.models import RecoveryRequest
from app.utils import parse_expire, gen_code
from app.database.database import Expired, NotFound, Revoked, db_client, AlreadyCreated
from fastapi import APIRouter, Depends, Header, Request
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/token", tags=["tokens"])


# recreate session token
@router.get("/recreate-tokens", dependencies=[Depends(require_origin), Depends(deny_bot)])
async def get_refresh_token(request: Request, user_agent:str = Header(default="")):
    fingerprint = request.state.fingerprint
    user_id = request.state.user_id
    
    if not fingerprint or not user_id:
        return JSONResponse({"detail":"Missing fingerprint or user_id"}, status_code=400)

    ip = request.client.host if request.client else "127.0.0.1"
    refresh_token = str(uuid.uuid4())
    
    session = await db_client.create_refresh_session(
        refresh_token=refresh_token,
        fingerprint=fingerprint,
        ip=ip,
        user_agent=user_agent,
        user_id=user_id,
    )
    
    access_token = AuthUtils.gen_jwt_token(user_id=request.state.user_id, session_id=session.id, role=str(request.state.role))
    resp = JSONResponse(content={"access_token": access_token}, status_code=200)

    resp.set_cookie(
        key="refresh_token",
        value=str(refresh_token),
        httponly=True,
        max_age=int(parse_expire(os.getenv("REFRESH_EXPIRE", "60d")).total_seconds()),
        secure=True,
        samesite="lax" 
    )
    return resp


# get jwt and update session token
@router.get("/get-tokens", dependencies=[Depends(require_origin)])
async def get_access_token(request: Request):
    fingerprint = request.state.fingerprint

    if not fingerprint:
        return JSONResponse({"detail":"Missing fingerprint"}, status_code=400)
    
    refresh_token = request.cookies.get("refresh_token")
    
    if not refresh_token:
        return JSONResponse({"detail":"Missing refresh token, make auth by /api/v1/auth/login /webapp or /api-key"}, status_code=400)

    ip = request.client.host if request.client else "127.0.0.1"
    
    try:
        session = await db_client.update_refresh_session(
            fingerprint=fingerprint, 
            ip=ip)
        
        user = await db_client.get_user(uid=str(session.user_id))
        
        access_token = AuthUtils.gen_jwt_token(user_id=user.id, session_id=session.id, role=str(user.role))
        resp = JSONResponse(content={"access_token": access_token}, status_code=200)
        
        resp.set_cookie(
            key="refresh_token",
            value=str(refresh_token),
            httponly=True,
            max_age=int(parse_expire(os.getenv("REFRESH_EXPIRE", "60d")).total_seconds()),
            secure=True,
            samesite="lax" 
        )
        
        return resp
    except (NotFound, Revoked, Expired):
        return JSONResponse({"detail":"Missing refresh token, make auth by /api/v1/auth/login /webapp or /api-key"}, status_code=400)

    
# revoke refresh session
@router.get("/revoke", dependencies=[Depends(require_origin), Depends(deny_bot)])
async def revoke_resresh_session(request: Request):
    fingerprint = request.state.fingerprint
    
    if not fingerprint:
        return JSONResponse({"detail":"Missing fingerprint"}, status_code=400)
        
    await db_client.revoke_refresh_session(fingerprint=fingerprint, revoked=True)
    
    return JSONResponse(content={"detail": "Token successfully revoked"}, status_code=200)


# generate recovery code
@router.get("/recovery", dependencies=[Depends(require_origin), Depends(require_auth)])
async def generate_recovery(request: Request):
    user_id = request.state.user_id
    
    if not user_id:
        return JSONResponse({"detail":"Missing user_id"}, status_code=400)
    
    try:
        code = gen_code(length=16)
        await db_client.create_recovery_code(user_id=user_id, code=code)
        try:
            await bot_websocket.send_json(message={"action":"send:recoverycode", "data":{"code": code}})
        except WSNotFound:
            return JSONResponse(content={"code": code}, status_code=500)
        return JSONResponse(content={"code": code}, status_code=200)
    except AlreadyCreated:
        return JSONResponse(content={"detail": "Code already generated"}, status_code=400)
    

# transfer user
@router.post("/transfer", dependencies=[Depends(require_origin), Depends(deny_bot)])
async def transfer_user(request_data: RecoveryRequest, request: Request):
    user_id = request.state.user_id
    
    if not user_id:
        return JSONResponse({"detail":"Missing user_id"}, status_code=400)
    try:
        await db_client.recovery_user(code=request_data.recovery_code, user_id=user_id)
        return JSONResponse(content={"detail": "Transfer successfull"}, status_code=200)
    except NotFound:
        return JSONResponse(content={"detail": "Recovery failed, user or recovery code not found"}, status_code=400)