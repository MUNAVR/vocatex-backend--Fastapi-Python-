from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from datetime import datetime
from . import models, schemas
from .models import *

class ChatService:
    async def create_message(self, message: schemas.MessageCreate, session: AsyncSession):
        print("here 1")
        Message = models.Message(
            sender_id=message.sender_id,
            receiver_id=message.receiver_id,
            content=message.content,
            timestamp=datetime.utcnow()
        )
        session.add(Message)
        await session.commit()
        await session.refresh(Message)
        return Message

    async def get_messages(self, receiver_id: str, sender_id: str, session: AsyncSession):
        statement = select(models.Message).where(
            models.Message.receiver_id == receiver_id,
            models.Message.sender_id == sender_id
        )
        result = await session.exec(statement)
        return result.all()   # Retrieve all matching messages
