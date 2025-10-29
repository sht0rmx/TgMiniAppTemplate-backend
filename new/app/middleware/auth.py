from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

import os, jwt
from app.utils import create_hash
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware



class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth = request.headers.get("authorization")

        if not auth:
            raise HTTPException(401, "Missing Authorization header")


        if auth.startswith("Bearer "):
            token = auth.split(" ")[1]
            
            try:
                payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=[str(os.getenv("JWT_ALG"))])
            except jwt.ExpiredSignatureError:
                return JSONResponse({"detail": "Token expired"}, status_code=401)
            except jwt.InvalidTokenError:
                return JSONResponse({"detail": "Invalid token"}, status_code=401)

            request.state.user_id = payload.get("sub")
            request.state.role = payload.get("role")
            request.state.session_id = payload.get("sid")

        elif auth.startswith("sk_"):
            key = auth.strip()
            key_hash = create_hash("API_SECRET", key)
            
            if os.getenv("API_TOKEN_HASH") != key_hash:
                raise HTTPException(401, "Api hash incorrect")
            
            request.state.user_id = payload.get("sub")
            request.state.role = payload.get("role")

        else:
            raise HTTPException(401, "Unsupported auth type")

        return await call_next(request)


class RoleMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        ...

        return await call_next(request)