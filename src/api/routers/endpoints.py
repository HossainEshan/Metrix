from fastapi import APIRouter

from src.api.routers.api_health import router as api_health_router
from src.api.routers.metrics import router as metrics_router

endpoints_router = APIRouter()

endpoints_router.include_router(api_health_router)
endpoints_router.include_router(metrics_router)
