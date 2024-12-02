import asyncio
from typing import List

from fastapi import Depends, WebSocket, WebSocketDisconnect


class WebsocketService:
    def __init__(self):
        self.connection = None

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connection = websocket

    async def disconnect(self):
        self.connection = None

    async def send_message(self, websocket: WebSocket, message: str):
        await websocket.send_text(message)


# Dependency function to get the WebsocketService
def get_websocket_service():
    return WebsocketService()


websocket_service_dependency = Depends(get_websocket_service)
