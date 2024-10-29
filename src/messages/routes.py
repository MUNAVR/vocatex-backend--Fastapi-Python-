from fastapi import APIRouter, WebSocket, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import List
from uuid import UUID
from src.db.main import get_session
from .models import Message
from .schemas import MessageCreate, MessageResponse
from .dependancies import *
from src.socket import socket_manager
from src.auth.utils import decode_token

messages_router = APIRouter()
access_token_bearer = AccessTokenBearer()

@messages_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    token = websocket.query_params.get("token")

    if not token:
        await websocket.close(code=403)
        return

    token_data = decode_token(token)
    if token_data is None:
        await websocket.close(code=403)
        return

    user_id = token_data.get("user", {}).get("user_uid")
    if user_id is None:
        await websocket.close(code=403)
        return

    await socket_manager.connect(websocket, user_id)

    try:
        while True:
            data = await websocket.receive_text()
    except Exception:
        pass
    finally:
        await socket_manager.disconnect(websocket)

@messages_router.post("/send_messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(
    message_create: MessageCreate,
    db: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer)
):
    if not socket_manager:
        raise HTTPException(status_code=500, detail="Socket Manager not initialized.")

    message = Message(**message_create.dict())
    message.sender_id = user_details['user']['user_uid']

    db.add(message)
    await db.commit()
    await db.refresh(message)

    await socket_manager.emit('chat_message', {
        'message': message_create.content,
        'sender_id': message.sender_id,
        'receiver_id': message.receiver_id
    }, to=message.receiver_id)

    return message

@messages_router.get("/{receiver_id}", response_model=List[MessageResponse])
async def get_messages(
    receiver_id: UUID,
    db: AsyncSession = Depends(get_session),
    token_data: dict = Depends(AccessTokenBearer())
):
    sender_id = token_data.get("user_id")
    if not sender_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sender ID not found in token")

    statement = select(Message).where(
        ((Message.sender_id == sender_id) & (Message.receiver_id == receiver_id)) |
        ((Message.sender_id == receiver_id) & (Message.receiver_id == sender_id))
    )
    results = await db.execute(statement)
    return results.scalars().all()
