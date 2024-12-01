from fastapi import APIRouter

from src.api.models.response import SystemMetrics
from src.api.services.metrics import MetricsService, metrics_service_dependency

router = APIRouter()


@router.get("/metrics", response_model=SystemMetrics)
async def get_metrics(service: MetricsService = metrics_service_dependency):
    response = service.get_system_metrics()
    return response
