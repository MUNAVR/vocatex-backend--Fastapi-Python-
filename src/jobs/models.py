from sqlmodel import SQLModel, Field, Relationship, Column
from datetime import datetime
import uuid
import sqlalchemy.dialects.postgresql as pg
from src.auth.models import ProviderUser
from typing import List


# JobDetails Table
class JobDetails(SQLModel, table=True):
    __tablename__ = "JobDetails"
    job_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, default=uuid.uuid4)
    )
    title: str
    description: str
    salary_from: float = Field(default=0)  
    salary_to: float = Field(default=0)    
    job_type: str = Field(nullable=False) 
    job_mode: str = Field(nullable=False) 
    job_location: str = Field(nullable=False)
    experience: str = Field(nullable=False)
    skills_and_requirements: str = Field(nullable=False)
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now)
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    )

    provider_id: uuid.UUID = Field(foreign_key="ProviderUser.uid", nullable=False)
    
    provider_user: "ProviderUser" = Relationship()
