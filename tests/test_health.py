import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.mark.asyncio
async def test_healthy(test_client):
    response = test_client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "Running"}
