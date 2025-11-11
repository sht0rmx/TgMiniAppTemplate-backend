import asyncio
import json

class SSEManager:
    def __init__(self):
        self.queues: dict[str, asyncio.Queue] = {}

    def get_queue(self, login_id: str) -> asyncio.Queue:
        if login_id not in self.queues:
            self.queues[login_id] = asyncio.Queue()
        return self.queues[login_id]

    async def push_event(self, login_id: str, data: dict):
        await self.get_queue(login_id).put(data)

    async def event_generator(self, login_id: str):
        queue = self.get_queue(login_id)
        print(f"[SSE] start stream for {login_id}")
        yield f"data: {json.dumps({'type': 'connected'})}\n\n"

        while True:
            try:
                event = await asyncio.wait_for(queue.get(), timeout=20)
                print(f"[SSE] sending {event}")
                yield f"data: {json.dumps(event)}\n\n"
            except TimeoutError:
                print(f"[SSE] keepalive {login_id}")
                yield ": keep-alive\n\n"


sse_manager = SSEManager()
