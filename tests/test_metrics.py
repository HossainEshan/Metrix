import pytest
from fastapi.testclient import TestClient

from src.api.services.metrics import get_metrics_service
from src.main import app


class MockMetricsService:

    def get_system_metrics(self):
        return {
            "cpu_usage_percent": 10.5,
            "memory_usage_percent": 55.2,
            "disk_usage_percent": 75.0,
            "swap_memory_usage_percent": 30.0,
            "network_sent_mbytes": 100.5,
            "network_received_mbytes": 200.0,
            "system_uptime": "12:34:56",
            "load_average": {"1_min": 0.5, "5_min": 0.7, "15_min": 0.8},
            "running_processes": 120,
        }


@pytest.fixture
def mock_metrics_service():

    def _callable():
        return MockMetricsService()

    return _callable


# Override the dependency
@pytest.fixture
def test_client(mock_metrics_service):
    app.dependency_overrides[get_metrics_service] = mock_metrics_service
    client = TestClient(app)
    yield client
    app.dependency_overrides = {}  # Cleanup after tests


def test_get_metrics(test_client):
    response = test_client.get("/metrics")
    assert response.status_code == 200
    data = response.json()

    # Validate the structure and values of the response
    assert data["cpu_usage_percent"] == 10.5
    assert data["memory_usage_percent"] == 55.2
    assert data["disk_usage_percent"] == 75.0
    assert data["swap_memory_usage_percent"] == 30.0
    assert data["network_sent_mbytes"] == 100.5
    assert data["network_received_mbytes"] == 200.0
    assert data["system_uptime"] == "12:34:56"
    assert data["load_average"]["1_min"] == 0.5
    assert data["load_average"]["5_min"] == 0.7
    assert data["load_average"]["15_min"] == 0.8
    assert data["running_processes"] == 120
