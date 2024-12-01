from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_api_health():
    response = client.get("/api_health")
    assert response.status_code == 200

    # Validate response is a dictionary of strings
    health_data = response.json()
    assert isinstance(health_data, dict)

    for api, status in health_data.items():
        assert isinstance(api, str)
        assert status in ["Healthy", "Error", "Down"]
