import httpx
from src.config import settings

# PROXY_URL = settings.flaresolver.proxy_url # d
TARGET_URL = settings.flaresolver.proxy_url  # p
HEADERS = {"Content-Type": "application/json", "X-Requested-With": "XMLHttpRequest"}


async def make_request(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            TARGET_URL,
            headers=HEADERS,
            json={
                "cmd": f"request.get",
                "url": url,
                "maxTimeout": 60000,
            },
        )
        return response.json()
