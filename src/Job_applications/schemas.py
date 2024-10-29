from pydantic import BaseModel,Field,EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional
from fastapi import UploadFile, File

class UserBasicDetails(BaseModel):
    first_name:str 
    last_name:str
    email:EmailStr

class JobComapanyDetails(BaseModel):
    job_title:str 
    company_name:str


class JobApplicationCreate(BaseModel):
    job_id:UUID
    resume_file: bytes = Field(..., description="Binary content of the PDF file")


class JobApplicationResponse(BaseModel):
    application_id: UUID
    user_id: UUID
    job_id: UUID
    status: str
    applied_at: datetime

    class Config:
        orm_mode = True

class AppliedJobResponse(BaseModel):
    application_id: UUID
    job_id: UUID
    job_title: str
    company_name: str
    status: str
    applied_at: datetime

    class Config:
        orm_mode = True

class JobApplicationResponsee(BaseModel):
    application_id: UUID
    job_id: UUID
    applicant_id:UUID
    job_title: str  # Change from UUID to str
    applicant_name: str
    applicant_email: EmailStr
    status: str
    applied_at: datetime

    class Config:
        orm_mode = True

class AcceptApplicationResponse(BaseModel):
    application_id: UUID
    status: str
    message: str