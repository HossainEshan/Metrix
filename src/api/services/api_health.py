from aiohttp import ClientSession

from src.api.routers.registry import service_registry
from src.api.services.base import BaseService


class APIHealthService(BaseService):
    async def get_api_health(self):
        urls = ["http://localhost:8000/status"]
        status = {}
        async with ClientSession() as client:
            for url in urls:
                try:
                    async with client.get(url) as response:
                        if response.status == 200:
                            status[url] = "Healthy"
                        else:
                            status[url] = "Error"
                except Exception as e:
                    status[url] = "Down"

        return status


service_registry.register(APIHealthService)
