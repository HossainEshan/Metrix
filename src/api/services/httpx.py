import httpx


def get_async_client():
    return httpx.AsyncClient()
