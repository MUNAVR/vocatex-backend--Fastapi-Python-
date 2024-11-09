from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from datetime import datetime
from . import models, schemas
from .models import *
from sqlalchemy import or_
from uuid import UUID



class ChatService:
    
    async def create_message(self, message: schemas.MessageCreate,sender_id:str, session: AsyncSession):
        print("here 1")
        
        # Create an instance of Message
        naive_created_at = datetime.now(timezone.utc).replace(tzinfo=None)
        message_instance = models.Message(
            sender_id=message.sender_id,
            receiver_id=message.receiver_id,
            content=message.content,
            created_at=naive_created_at  # Make sure to use timezone-aware timestamp
        )
        
        # Add and commit the message to the database
        session.add(message_instance)
        await session.commit()
        
        # Refresh to load the new message details
        await session.refresh(message_instance)
        
        return message_instance

    async def get_messages(self, receiver_id: UUID, sender_id: UUID, db: AsyncSession):
        try:
            result = await db.execute(
                select(Message).where(
                    or_(
                        (Message.sender_id == sender_id) & (Message.receiver_id == receiver_id),
                        (Message.sender_id == receiver_id) & (Message.receiver_id == sender_id)
                    )
                ).order_by(Message.created_at)
            )
            return result.scalars().all()
        except Exception as e:
            print(f"Error retrieving messages: {e}")
            return []  # Retrieve all matching messages
