import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import WebSocket

from src.api.services.api_health import APIHealthService
from src.api.services.metrics import MetricsService
from src.api.services.websocket import WebsocketService


@pytest.fixture
def mock_metrics_service():
    service = MagicMock(spec=MetricsService)
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
    service = AsyncMock(spec=APIHealthService)
    service.get_api_health.return_value = {
        "test_endpoint_1": "Healthy",
        "test_endpoint_2": "Error",
        "test_endpoint_3": "Down",
    }
    return service


@pytest.fixture
def mock_websocket_service(mock_metrics_service, mock_api_health_service):
    service = WebsocketService()
    service.metrics_service = mock_metrics_service
    service.api_health_service = mock_api_health_service
    return service


@pytest.fixture
def mock_websocket():
    websocket = AsyncMock(spec=WebSocket)
    return websocket


@pytest.mark.asyncio
async def test_websocket_connect(mock_websocket_service, mock_websocket):
    await mock_websocket_service.connect(mock_websocket)
    mock_websocket.accept.assert_called_once()


@pytest.mark.asyncio
async def test_send_metrics(
    mock_websocket_service, mock_websocket, mock_metrics_service
):
    # Set up flag to run only once
    flag = True

    def set_flag_false():
        nonlocal flag
        flag = False

    # Mock sleep to set flag false after first iteration
    with patch("asyncio.sleep", AsyncMock(side_effect=set_flag_false)):
        await mock_websocket_service.send_metrics(mock_websocket, flag)

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
    mock_websocket_service, mock_websocket, mock_api_health_service
):
    # Set up flag to run only once
    flag = True

    def set_flag_false():
        nonlocal flag
        flag = False

    # Mock sleep to set flag false after first iteration
    with patch("asyncio.sleep", AsyncMock(side_effect=set_flag_false)):
        await mock_websocket_service.send_api_health(mock_websocket, flag)

    mock_api_health_service.get_api_health.assert_called_once()
    mock_websocket.send_text.assert_called_once_with(
        json.dumps(
            {
                "test_endpoint_1": "Healthy",
                "test_endpoint_2": "Error",
                "test_endpoint_3": "Down",
            }
        )
    )


@pytest.mark.asyncio
async def test_send_cancelled(mock_websocket_service, mock_websocket):
    # Test for send_metrics cancellation
    with patch("asyncio.sleep", AsyncMock(side_effect=asyncio.CancelledError)):
        await mock_websocket_service.send_metrics(mock_websocket, True)

    # Test for send_api_health cancellation
    with patch("asyncio.sleep", AsyncMock(side_effect=asyncio.CancelledError)):
        await mock_websocket_service.send_api_health(mock_websocket, True)

    # No assertions needed - test passes if no exception is raised


@pytest.mark.asyncio
async def test_false_flag(
    mock_websocket_service,
    mock_websocket,
    mock_api_health_service,
    mock_metrics_service,
):
    # Set up flag to run only once
    flag = False

    # Call the send_api_health method with the false flag
    await mock_websocket_service.send_api_health(mock_websocket, flag)

    # Call the send_metrics method with the false flag
    await mock_websocket_service.send_metrics(mock_websocket, flag)

    # Verify that the API health service was not called
    mock_api_health_service.get_api_health.assert_not_called()
    # Verify that the metrics service was not called
    mock_metrics_service.get_system_metrics.assert_not_called()
    # Verify that the websocket did not send any message
    mock_websocket.send_text.assert_not_called()
