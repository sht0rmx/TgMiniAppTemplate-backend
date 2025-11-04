from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from app.database.database import db_client
from app.middleware.auth import require_origin, deny_bot, require_auth
from app.utils import parse_user_agent_data


router = APIRouter(prefix="/session", tags=["Sessions"])

@router.get("/current", dependencies=[Depends(require_origin), Depends(require_auth)])
async def current_session(request: Request):
    session_id = request.state.session_id
    fingerprint = request.state.fingerprint
    
    if not session_id:
        return JSONResponse({"detail": "session id not found"})
    
    session = await db_client.get_refresh_session(fingerprint=fingerprint)
    
    info = parse_user_agent_data(str(session.user_agent))
    return JSONResponse({"ip": session.ip, "lastUsed": session.used_at.isoformat(), "info": info})
    
@router.get("/all", dependencies=[Depends(require_origin), Depends(require_auth)])
async def all_sessions(request: Request):
    ...
    
@router.get("/kill/{sid}", dependencies=[Depends(require_origin), Depends(deny_bot)])
async def kill_session(request: Request):
    ...