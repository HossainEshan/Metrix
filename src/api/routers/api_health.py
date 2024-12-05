from fastapi import APIRouter, Depends

from src.api.services.api_health import APIHealthService
from src.api.services.registry import service_registry

router = APIRouter()


@router.get("/api_health")
async def api_health(
    service: APIHealthService = Depends(service_registry.get(APIHealthService)),
):
    print("\nDependency key in router:", service)
    response = await service.get_api_health()
    return response
