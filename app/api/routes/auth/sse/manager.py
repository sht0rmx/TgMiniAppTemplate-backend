import asyncio
import json
from typing import Dict

class SSEManager:
    def __init__(self):
        self.queues: Dict[str, asyncio.Queue] = {}

    def get_queue(self, login_id: str) -> asyncio.Queue:
        if login_id not in self.queues:
            self.queues[login_id] = asyncio.Queue()
        return self.queues[login_id]

    async def push_event(self, login_id: str, data: dict):
        await self.get_queue(login_id).put(data)

    async def event_generator(self, login_id: str):
        queue = self.get_queue(login_id)
        while True:
            event = await queue.get()
            yield f"data: {json.dumps(event)}\n\n"
            
sse_manager = SSEManager()