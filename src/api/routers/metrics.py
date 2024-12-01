from fastapi import APIRouter

from src.api.models.response import SystemMetrics
from src.api.repository.metrics import MetricsRepository

router = APIRouter()


@router.get("/metrics", response_model=SystemMetrics)
async def get_metrics():
    response = MetricsRepository.get_system_metrics()
    return response
