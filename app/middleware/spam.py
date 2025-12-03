from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.database.redis import redis_client


class RateLimitMiddleware:
    def __init__(self, app: FastAPI, limit: int = 5, period: int = 10):
        self.app = app
        self.limit = limit
        self.period = period

    async def __call__(self, request: Request, call_next):
        if request.method == "OPTIONS":
            return await call_next(request)

        ip = request.client.host if request.client else ""
        key = f"rate:{ip}"
        count = await redis_client.get(key)

        if count is None:
            await redis_client.set_(key, 1, ex=self.period)
        elif int(count) < self.limit:
            await redis_client.incr(key)
        else:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too Many Requests"}
            )

        response = await call_next(request)
        return response
