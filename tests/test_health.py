from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_healthy():
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "Running"}
