from fastapi.testclient import TestClient
from pydantic import ValidationError

from src.api.models.response import SystemMetrics
from src.main import app

client = TestClient(app)


def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200

    # Parse response JSON into SystemMetrics model
    try:
        metrics = SystemMetrics(**response.json())
    except ValidationError as e:
        assert False, f"Response validation failed: {e}"

    # Check that the values make sense
    assert metrics.cpu_usage_percent >= 0.0
    assert metrics.memory_usage_percent >= 0.0
    assert metrics.disk_usage_percent >= 0.0
    assert metrics.network_sent_mbytes >= 0.0
    assert metrics.network_received_mbytes >= 0.0
    assert isinstance(metrics.system_uptime, str)
    assert isinstance(metrics.load_average, dict)
    assert isinstance(metrics.running_processes, int)
    assert metrics.swap_memory_usage_percent >= 0.0
