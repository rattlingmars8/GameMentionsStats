from fastapi import APIRouter

from src.config import settings
from api.api_V1.game_mentions import router as game_router

router = APIRouter(prefix=settings.api_prefix.v1.prefix)

router.include_router(game_router, prefix=settings.api_prefix.v1.game_data)
