import asyncio
import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.api.services.api_health import APIHealthService, api_health_service_dependency
from src.api.services.metrics import MetricsService, metrics_service_dependency
from src.api.services.websocket import WebsocketService, websocket_service_dependency

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    websocket_service: WebsocketService = websocket_service_dependency,
    metrics_service: MetricsService = metrics_service_dependency,
    api_health_service: APIHealthService = api_health_service_dependency,
):
    await websocket_service.connect(websocket)

    # Create a cancellation group for tasks
    flag = True

    try:
        # Create and track metrics task
        metrics_task = asyncio.create_task(
            send_metrics(websocket, websocket_service, metrics_service, flag)
        )

        # Create and track API health task
        health_task = asyncio.create_task(
            send_api_health(websocket, websocket_service, api_health_service, flag)
        )

        while True:
            try:
                # Receive messages to keep the WebSocket connection alive
                await websocket.receive_text()
            except WebSocketDisconnect:
                print("WebSocket disconnected by client.")
                break

    except Exception as e:
        print(f"Unhandled WebSocket exception: {e}")

    finally:
        # Ensure cleanup
        print("Cleanup started.")
        flag = False  # Stop all tasks
        metrics_task.cancel()
        health_task.cancel()
        await api_health_service.close()
        await websocket_service.disconnect()
        print("Cleanup completed.")


async def send_metrics(
    websocket: WebSocket,
    websocket_service: WebsocketService,
    metrics_service: MetricsService,
    flag,
):
    try:
        while flag:
            metrics_data = metrics_service.get_system_metrics()
            await websocket_service.send_message(websocket, json.dumps(metrics_data))
            print("Sent Metrics")
            await asyncio.sleep(0.5)
    except asyncio.CancelledError:
        print("Metrics task cancelled")
    except Exception as e:
        print("Error: Metrics task", e)


async def send_api_health(
    websocket: WebSocket,
    websocket_service: WebsocketService,
    api_health_service: APIHealthService,
    flag,
):
    try:
        while flag:
            api_health_data = await api_health_service.get_api_health()
            await websocket_service.send_message(websocket, json.dumps(api_health_data))
            print("Sent API Health")
            await asyncio.sleep(5)
    except asyncio.CancelledError:
        print("API Health task cancelled")
    except Exception as e:
        print("Error: API Health task", e)
