import socketio
from fastapi import FastAPI
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from .models import Message
from .service import ChatService
from .schemas import MessageCreate
from src.db.main import get_session
from datetime import datetime, timezone
from contextlib import asynccontextmanager

chat_service = ChatService()
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=["http://localhost:4200"])  # Allow frontend URL
app = FastAPI()
app.mount("/ws", socketio.ASGIApp(sio))  



@asynccontextmanager
async def get_async_session():
    """Custom context manager for AsyncSession."""
    async_session = await get_session()
    try:
        yield async_session
    finally:
        await async_session.close()

@sio.event
async def connect(sid, environ):
    print("Client connected:", sid)

@sio.event
async def disconnect(sid):
    print("Client disconnected:", sid)

@sio.event
async def message(sid, data: dict):
    print("Received message from client:", data)
    try:
        # Parse the incoming data into the MessageCreate schema
        message_data = MessageCreate(**data)
        
        # Manually create a session and pass it to the service
        async with get_async_session() as db:
            saved_message = await chat_service.create_message(message_data, db)
        
        # Emit the saved message to the specified room (receiver_id)
        await sio.emit('chat_message', {
            "sender_id": str(saved_message.sender_id),
            "receiver_id": str(saved_message.receiver_id),
            "content": saved_message.content,
            "timestamp": saved_message.created_at.isoformat()
        }, room=str(saved_message.receiver_id))
        
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        await sio.emit('error', {'error': 'Failed to save message due to database error.'})
    except Exception as e:
        print(f"General error handling message: {e}")
        await sio.emit('error', {'error': 'Failed to process message due to an unexpected error.'})
