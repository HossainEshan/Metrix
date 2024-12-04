from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from src.api.routers.registry import service_registry
from src.api.services.api_health import APIHealthService
from src.main import app


@pytest.fixture
def api_health_service():
    service = AsyncMock(spec=APIHealthService)
    service.get_api_health.return_value = {
        "test_endpoint_1": "Healthy",
        "test_endpoint_2": "Error",
        "test_endpoint_3": "Down",
    }
    print("\nMocked service created:", service)
    return service


@pytest.fixture
def test_client(api_health_service):
    print("\nAttempting to override dependency...")
    print("Service registry key:", service_registry.get(APIHealthService))

    # Get the actual dependency that's being used in the router
    dependency_key = service_registry.get(APIHealthService)
    print("Current dependency:", app.dependency_overrides.get(dependency_key))

    # Override the dependency
    app.dependency_overrides[dependency_key] = lambda: api_health_service
    print("Dependency override set")
    print("After override:", app.dependency_overrides)

    client = TestClient(app)
    yield client
    app.dependency_overrides = {}


@pytest.mark.asyncio
async def test_get_api_health_endpoint(test_client, api_health_service):
    # Given: Known mock response data
    expected_data = {
        "test_endpoint_1": "Healthy",
        "test_endpoint_2": "Error",
        "test_endpoint_3": "Down",
    }

    # Print the mock's configured return value
    print(
        "\nMock configured to return:", api_health_service.get_api_health.return_value
    )

    # When: Making a request to the API health endpoint
    response = test_client.get("/api_health")

    # Print the actual response
    print("Actual response:", response.json())

    # Then: Response should be successful
    assert response.status_code == 200

    # And: Response should match the mock service data
    data = response.json()
    assert data == expected_data

    # Verify the mock was called
    api_health_service.get_api_health.assert_called_once()
