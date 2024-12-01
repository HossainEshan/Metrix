from fastapi import APIRouter

from src.api.models.response import SystemMetrics
from src.api.repository.api_health import APIHealthRespository

router = APIRouter()


@router.get("/api_health")
async def api_health():

    response = await APIHealthRespository.get_api_health()
    return response
