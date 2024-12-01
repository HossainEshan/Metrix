from fastapi import APIRouter

from src.api.services.api_health import APIHealthService, api_health_service_dependency

router = APIRouter()


@router.get("/api_health")
async def api_health(service: APIHealthService = api_health_service_dependency):

    response = await service.get_api_health()
    return response
