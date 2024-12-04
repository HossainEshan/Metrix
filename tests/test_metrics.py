from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from src.api.routers.registry import service_registry
from src.api.services.metrics import MetricsService
from src.main import app


@pytest.fixture
def metrics_service():
    service = MagicMock(spec=MetricsService)
    service.get_system_metrics.return_value = {
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
    return service


@pytest.fixture
def test_client(metrics_service):
    app.dependency_overrides[service_registry.get(MetricsService)] = (
        lambda: metrics_service
    )
    client = TestClient(app)
    yield client
    app.dependency_overrides = {}


@pytest.mark.asyncio
async def test_get_metrics(test_client, metrics_service):

    expected_metrics = metrics_service.get_system_metrics.return_value

    response = test_client.get("/metrics")
    assert response.status_code == 200
    data = response.json()

    assert data == expected_metrics

    # Validate specific values
    assert isinstance(data["cpu_usage_percent"], float)
    assert isinstance(data["memory_usage_percent"], float)
    assert isinstance(data["load_average"], dict)
    assert len(data["load_average"]) == 3
    assert isinstance(data["running_processes"], int)

    # Verify the mock was called
    metrics_service.get_system_metrics.assert_called_once()
