import asyncio

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from app.api.routes.auth.sse.manager import sse_manager

router = APIRouter(prefix="/sse", tags=["sse"])


@router.get("/check/{login_id}")
async def sse_endpoint(request: Request, login_id: str):
    async def event_stream():
        try:
            async for event in sse_manager.event_generator(login_id):
                yield event
        except asyncio.CancelledError:
            print(f"Client disconnected: {login_id}")

    return StreamingResponse(event_stream(), media_type="text/event-stream")
