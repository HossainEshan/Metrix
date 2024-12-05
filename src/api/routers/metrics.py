from fastapi import APIRouter, Depends

from src.api.models.response import SystemMetrics
from src.api.services.metrics import MetricsService
from src.api.services.registry import service_registry

router = APIRouter()


@router.get("/metrics", response_model=SystemMetrics)
async def get_metrics(
    service: MetricsService = Depends(service_registry.get(MetricsService)),
):
    response = service.get_system_metrics()
    return response
