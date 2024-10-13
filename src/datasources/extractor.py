import aiohttp
from abc import ABC, abstractmethod

class Extractor(ABC):
    def __init__(self, config: str) -> str:
        self.base_url = config["the_guardian_url"]
        self.session = aiohttp.ClientSession()

    async def fetch(self, url: str) -> str:
        async with self.session.get(url) as response:
            response.raise_for_status()
            return await response.text()

    @abstractmethod
    async def extract(self):
        pass

    async def close(self):
        await self.session.close()