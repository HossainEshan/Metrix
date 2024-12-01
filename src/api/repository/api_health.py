import httpx


class APIHealthRespository:

    async def get_api_health():
        urls = ["http://localhost:8000/status"]
        status = {}
        async with httpx.AsyncClient() as client:
            for url in urls:
                try:
                    response = await client.get(url, timeout=5)
                    status[url] = "Healthy" if response.status_code == 200 else "Error"
                except Exception:
                    status[url] = "Down"
        return status
