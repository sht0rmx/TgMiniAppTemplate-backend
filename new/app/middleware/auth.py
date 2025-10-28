from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

import os, jwt, hmac, hashlib
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware



class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, req: Request, call_next):
        auth = req.headers.get("authorization")

        if not auth:
            raise HTTPException(401, "Missing Authorization header")


        if auth.startswith("Bearer "):
            token = auth.split(" ")[1]
            ...


        elif auth.startswith("sk_"):
            key = auth.strip()
            ...

        else:
            raise HTTPException(401, "Unsupported auth type")

        return await call_next(req)


class RoleMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, req: Request, call_next):
        ...

        return await call_next(req)