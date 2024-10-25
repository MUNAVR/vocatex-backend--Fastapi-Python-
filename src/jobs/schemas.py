from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


class JobCreate(BaseModel):
    title: str
    description: str
    salary_from: float  
    salary_to: float    
    job_type: str 
    job_mode: str      
    job_location: str   
    experience: str     
    skills_and_requirements: str 
     


class JobRead(BaseModel):
    job_id: UUID
    title: str
    description: str
    salary_from: float  
    salary_to: float    
    job_type: str 
    job_mode: str      
    job_location: str   
    experience: str     
    skills_and_requirements: str  
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True 


class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    salary_from: Optional[float] = None
    salary_to: Optional[float] = None
    job_type: Optional[str] = None
    job_model: Optional[str] = None
    job_location: Optional[str] = None
    experience: Optional[str] = None
    skills_and_requirements: Optional[str] = None