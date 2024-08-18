import httpx
from src.config import settings

PROXY_URL = settings.flaresolver.proxy_url
HEADERS = {"Content-Type": "application/json", "X-Requested-With": "XMLHttpRequest"}


async def make_request(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            PROXY_URL,
            headers=HEADERS,
            json={
                "cmd": f"request.get",
                "url": url,
                "maxTimeout": 60000,
            },
        )
        return response.json()
