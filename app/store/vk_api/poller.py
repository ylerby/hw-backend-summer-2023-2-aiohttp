import asyncio
import typing
from asyncio import Task
from typing import Optional

if typing.TYPE_CHECKING:
    from app.web.app import Application


class Poller:
    def __init__(self, app: "Application"):
        self.app = app
        self.is_running = False
        self.poll_task: Optional[Task] = None

    async def start(self):
        self.is_running = True
        self.poll_task = asyncio.create_task(self.poll())

    async def stop(self):
        self.is_running = False
        await self.poll_task

    async def poll(self):
        while self.is_running:
            updates = await self.app.store.vk_api.poll()
            await self.app.store.bots_manager.handle_updates(updates)