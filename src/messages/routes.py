from fastapi import APIRouter, WebSocket, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, Session
from typing import List
from uuid import UUID
from src.db.main import get_session
from .models import Message
from .schemas import MessageSchema
from .service import ChatService

from src.auth.utils import decode_token
from .socket_server import sio, app as socket_app


messages_router = APIRouter()
ChatService=ChatService()


@messages_router.get("/messages/{receiver_id}", response_model=List[MessageSchema])
async def get_chat_history(receiver_id: UUID, sender_id: UUID, db: AsyncSession = Depends(get_session)):
    messages = await ChatService.get_messages(receiver_id, sender_id, db)  # Ensure correct order of parameters
    if not messages:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Messages not found")
    return messages


