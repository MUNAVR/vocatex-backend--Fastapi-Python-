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
        orm_mode = True
