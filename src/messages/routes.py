# src/messages/routes.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict
from uuid import UUID
from src.db.main import get_session
from .models import Message
from .schemas import MessageSchema, MessageCreate
from .service import ChatService
from src.auth.utils import decode_token
from fastapi import Query

# Initialize APIRouter and ChatService
messages_router = APIRouter()
chat_service = ChatService()

# Dictionary to manage active WebSocket connections by user ID
active_connections: Dict[UUID, List[WebSocket]] = {}

# Dependency to authenticate and get user ID from token
async def get_current_user_id(token: str):
    payload = decode_token(token)
    return UUID(payload.get("user_id"))

# Function to connect WebSocket and manage active connections
async def connect_user(user_id: UUID, websocket: WebSocket):
    if user_id not in active_connections:
        active_connections[user_id] = []
    active_connections[user_id].append(websocket)
    await websocket.accept()

# Function to disconnect WebSocket
async def disconnect_user(user_id: UUID, websocket: WebSocket):
    if user_id in active_connections:
        active_connections[user_id].remove(websocket)
        if not active_connections[user_id]:  # Remove user if no active connections
            del active_connections[user_id]

# Function to send message to a specific user
async def send_personal_message(user_id: UUID, message: MessageSchema):
    if user_id in active_connections:
        for connection in active_connections[user_id]:
            await connection.send_json(message.dict())


# REST API route to fetch chat history
@messages_router.get("/{receiver_id}", response_model=List[MessageSchema])
async def get_chat_history(
    receiver_id: UUID, 
    sender_id: UUID = Query(...),  
    db: AsyncSession = Depends(get_session)
):
    messages = await chat_service.get_messages(receiver_id, sender_id, db)
    if not messages:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Messages not found")
    return messages
