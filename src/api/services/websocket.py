import asyncio
import json

from fastapi import WebSocket

from src.api.routers.registry import service_registry
from src.api.services.api_health import APIHealthService
from src.api.services.base import BaseService
from src.api.services.metrics import MetricsService


class WebsocketService(BaseService):
    def __init__(self):
        self.metrics_service: MetricsService = None
        self.api_health_service: APIHealthService = None

    async def connect(self, websocket: WebSocket):
        await websocket.accept()

    async def send_metrics(self, websocket: WebSocket, flag: bool):
        """Send system metrics to the websocket client"""
        try:
            while flag:
                metrics_data = self.metrics_service.get_system_metrics()
                await websocket.send_text(json.dumps(metrics_data))
                print("Sent Metrics")
                await asyncio.sleep(0.5)
        except asyncio.CancelledError:
            print("Metrics task cancelled")
        except Exception as e:
            print(f"Error: Metrics task - {e}")

    async def send_api_health(self, websocket: WebSocket, flag: bool):
        """Send API health data to the websocket client"""
        try:
            while flag:
                api_health_data = await self.api_health_service.get_api_health()
                await websocket.send_text(json.dumps(api_health_data))
                print("Sent API Health")
                await asyncio.sleep(5)
        except asyncio.CancelledError:
            print("API Health task cancelled")
        except Exception as e:
            print(f"Error: API Health task - {e}")


service_registry.register(WebsocketService)
