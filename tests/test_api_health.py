import pytest
from fastapi.testclient import TestClient

from src.api.services.api_health import get_api_health_service
from src.main import app


class MockAPIHealthService:

    async def get_api_health(self):
        return {
            "test_endpoint_1": "Healthy",
            "test_endpoint_2": "Error",
            "test_endpoint_3": "Down",
        }


@pytest.fixture
def mock_api_health_service():

    def _callable():
        return MockAPIHealthService()

    return _callable


# Override the dependency
@pytest.fixture
def test_client(mock_api_health_service):
    app.dependency_overrides[get_api_health_service] = mock_api_health_service
    client = TestClient(app)
    yield client
    app.dependency_overrides = {}  # Cleanup after tests


def test_api_health(test_client):
    response = test_client.get("/api_health")
    assert response.status_code == 200

    # Validate response is a dictionary of strings
    data = response.json()
    assert data["test_endpoint_1"] == "Healthy"
    assert data["test_endpoint_2"] == "Error"
    assert data["test_endpoint_3"] == "Down"
