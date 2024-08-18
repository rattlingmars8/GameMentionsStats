from fastapi import APIRouter

from .api_V1 import router as router_api_V1

router = APIRouter()


router.include_router(router_api_V1)
