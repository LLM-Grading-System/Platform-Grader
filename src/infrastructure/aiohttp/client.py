from typing import Any, AsyncGenerator

import aiohttp
from aiohttp import ClientSession


async def get_session() -> AsyncGenerator[ClientSession, Any]:
    async with aiohttp.ClientSession() as session:
        yield session
