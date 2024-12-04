import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import WebSocket

from src.api.services.websocket import WebsocketService


@pytest.fixture
def mock_metrics_service():
    service = MagicMock()
    service.get_system_metrics.return_value = {
        "cpu_usage_percent": 50.0,
        "memory_usage_percent": 60.0,
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
def mock_api_health_service():
    service = AsyncMock()
    service.get_api_health.return_value = {"http://localhost:8000/status": "Healthy"}
    return service


@pytest.fixture
def websocket_service(mock_metrics_service, mock_api_health_service):
    service = WebsocketService()
    service.metrics_service = mock_metrics_service
    service.api_health_service = mock_api_health_service
    return service


@pytest.fixture
def mock_websocket():
    websocket = AsyncMock(spec=WebSocket)
    return websocket


@pytest.mark.asyncio
async def test_websocket_connect(websocket_service, mock_websocket):
    await websocket_service.connect(mock_websocket)
    mock_websocket.accept.assert_called_once()


@pytest.mark.asyncio
async def test_send_metrics(websocket_service, mock_websocket, mock_metrics_service):
    # Set up flag to run only once
    flag = True

    def set_flag_false():
        nonlocal flag
        flag = False

    # Mock sleep to set flag false after first iteration
    with patch("asyncio.sleep", AsyncMock(side_effect=set_flag_false)):
        await websocket_service.send_metrics(mock_websocket, flag)

    mock_metrics_service.get_system_metrics.assert_called_once()
    mock_websocket.send_text.assert_called_once_with(
        json.dumps(
            {
                "cpu_usage_percent": 50.0,
                "memory_usage_percent": 60.0,
                "disk_usage_percent": 75.0,
                "swap_memory_usage_percent": 30.0,
                "network_sent_mbytes": 100.5,
                "network_received_mbytes": 200.0,
                "system_uptime": "12:34:56",
                "load_average": {"1_min": 0.5, "5_min": 0.7, "15_min": 0.8},
                "running_processes": 120,
            }
        )
    )


@pytest.mark.asyncio
async def test_send_api_health(
    websocket_service, mock_websocket, mock_api_health_service
):
    # Set up flag to run only once
    flag = True

    def set_flag_false():
        nonlocal flag
        flag = False

    # Mock sleep to set flag false after first iteration
    with patch("asyncio.sleep", AsyncMock(side_effect=set_flag_false)):
        await websocket_service.send_api_health(mock_websocket, flag)

    mock_api_health_service.get_api_health.assert_called_once()
    mock_websocket.send_text.assert_called_once_with(
        json.dumps({"http://localhost:8000/status": "Healthy"})
    )


@pytest.mark.asyncio
async def test_send_metrics_cancelled(websocket_service, mock_websocket):
    with patch("asyncio.sleep", AsyncMock(side_effect=asyncio.CancelledError)):
        await websocket_service.send_metrics(mock_websocket, True)
    # No assertions needed - test passes if no exception is raised


@pytest.mark.asyncio
async def test_send_api_health_cancelled(websocket_service, mock_websocket):
    with patch("asyncio.sleep", AsyncMock(side_effect=asyncio.CancelledError)):
        await websocket_service.send_api_health(mock_websocket, True)
    # No assertions needed - test passes if no exception is raised
