from fastapi import WebSocket
from fastapi_socketio import SocketManager
from uuid import UUID
from typing import Optional
from fastapi import FastAPI

class CustomSocketManager(SocketManager):
    connections: dict = {}

    async def connect(self, websocket: WebSocket, user_id: UUID):
        await super().connect(websocket)
        self.connections[websocket] = user_id  # Store connection by user ID

    async def disconnect(self, websocket: WebSocket):
        await super().disconnect(websocket)
        if websocket in self.connections:
            del self.connections[websocket]  # Remove connection when disconnected

    async def emit(self, event: str, data: dict, to: Optional[UUID] = None):
        if to:
            # Emit to specific user ID
            for ws, uid in self.connections.items():
                if uid == to:
                    await super().emit(event, data, room=ws)
                    return
        else:
            # Broadcast to all connected clients
            await super().emit(event, data)

socket_manager: Optional[CustomSocketManager] = None

def initialize_socket_manager(app: FastAPI) -> CustomSocketManager:
    global socket_manager
    socket_manager = CustomSocketManager(app)
    return socket_manager
