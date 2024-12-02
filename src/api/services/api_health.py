from aiohttp import ClientSession
from fastapi import Depends


class APIHealthService:
    def __init__(self):
        self.client = ClientSession()

    async def get_api_health(self):
        urls = ["http://localhost:8000/status"]
        status = {}

        for url in urls:
            try:
                async with self.client.get(url) as response:
                    if response.status == 200:
                        status[url] = "Healthy"
                    else:
                        status[url] = "Error"
            except Exception as e:
                status[url] = "Down"
                print("API HS Exception", e)

        return status

    async def close(self):
        await self.client.close()


# Dependency
async def get_api_health_service():
    return APIHealthService()


api_health_service_dependency = Depends(get_api_health_service)
