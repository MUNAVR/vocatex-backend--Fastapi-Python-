from sqlmodel import SQLModel, Field, Column
from datetime import datetime
import uuid
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy.orm import relationship
from src.job_seeker.models import *
from typing import List

class User (SQLModel, table=True):
    __tablename__ = "User"
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False, 
            primary_key=True,
            default=uuid.uuid4  
        )
    )
    username:str
    email:str
    is_verified:bool = False
    password_hash:str = Field(exclude=True)
    otp:str 
    otp_created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now) 
    )
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now) 
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now, onupdate=datetime.now) 
    )
    
    applications: List["JobApplication"] = Relationship(back_populates="applicant")


    def __repr__(self):
        return f"<User {self.username}>"
    
    
class ProviderUser (SQLModel, table=True):
    __tablename__ = "ProviderUser"
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False, 
            primary_key=True,
            default=uuid.uuid4  
        )
    )
    username:str
    email:str
    is_verified:bool = False
    otp:str 
    otp_created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now) 
    )
    password_hash:str = Field(exclude=True)
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now) 
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now, onupdate=datetime.now) 
    )

    def __repr__(self):
        return f"<User {self.username}>"