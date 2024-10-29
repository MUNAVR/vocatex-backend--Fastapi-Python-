from pydantic import BaseModel
import uuid
from datetime import datetime

class MessageCreate(BaseModel):
    receiver_id: uuid.UUID 
    content: str

class MessageResponse(BaseModel):
    id: uuid.UUID
    sender_id: uuid.UUID
    receiver_id: uuid.UUID
    content: str

    class Config:
        from_attributes = True


class MessageBase(BaseModel):
    sender_id: str
    receiver_id: str
    content: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class MessageSchema(BaseModel):
    uid: uuid.UUID
    content: str
    created_at: datetime
    sender_id: uuid.UUID
    receiver_id: uuid.UUID

    class Config:
        orm_mode = True