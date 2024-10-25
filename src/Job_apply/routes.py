from fastapi import APIRouter,Depends,status,File,Form
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import User,ProviderUser
from src.job_seeker.models import *
from src.jobs.models import JobDetails
from typing import List
from uuid import UUID,uuid4
from src.db.main import get_session
from .dependancies import *
from .schemas import *
from sqlalchemy import select
from .models import JobApplication


apply_router = APIRouter()
access_token_bearer=AccessTokenBearer()

@apply_router.get('/get_user_details', response_model=UserBasicDetails, status_code=status.HTTP_200_OK)
async def get_user_details(
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer)
):
    uid = user_details['user']['user_uid']


    user = await session.get(User, uid)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    resume = await session.execute(
        select(ResumeDetails).where(ResumeDetails.user_id == uid)
    )
    resume = resume.scalar_one_or_none()
    
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
    
    personal_info = await session.execute(
        select(PersonalInfo).where(PersonalInfo.resume_id == resume.resume_id)
    )
    personal_info = personal_info.scalar_one_or_none()

    if not personal_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personal information not found")

    return {
        "first_name": personal_info.first_name,
        "last_name": personal_info.last_name,
        "email": user.email
    }


@apply_router.get('/get_job_details/{job_id}', response_model=JobComapanyDetails, status_code=status.HTTP_200_OK)
async def get_job_details(
    job_id: UUID,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer)
):
    
    job = await session.get(JobDetails, job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    provider = await session.get(ProviderUser, job.provider_id)
    if not provider:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company information not found")

    return {
        "job_title": job.title,
        "company_name": provider.username
    }

    

from fastapi import UploadFile, File

@apply_router.post('/create/application/{job_id}', response_model=JobApplicationResponse, status_code=status.HTTP_201_CREATED)
async def create_job_application(
    job_id: UUID,
    resume_file: UploadFile = File(...),  # 10MB max size
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer)
):
    uid = user_details['user']['user_uid']
    user = await session.get(User, uid)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    job = await session.get(JobDetails, job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    
    # Access filename correctly now that resume_file is UploadFile
    if not resume_file.filename.endswith(('.pdf', '.doc', '.docx')):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF or Word documents are allowed.")
    
    resume_content = await resume_file.read()  # Read the file content as bytes

    new_application = JobApplication(
        user_id=uid,
        job_id=job_id,
        resume_file=resume_content,  # Save the resume file content (bytes)
        status="pending",
        applied_at=datetime.now()
    )
    
    session.add(new_application)
    await session.commit()
    await session.refresh(new_application)
    return new_application


@apply_router.get('/get_applied_jobs', response_model=List[AppliedJobResponse], status_code=status.HTTP_200_OK)
async def get_applied_jobs(
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer)
):
    uid = user_details['user']['user_uid']
    
    # Fetch the applied jobs for the user
    applications = await session.execute(
        select(JobApplication).where(JobApplication.user_id == uid)
    )
    applications = applications.scalars().all()

    if not applications:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No applied jobs found")

    # Fetch job details and provider information for each application
    applied_jobs = []
    for application in applications:
        job = await session.get(JobDetails, application.job_id)
        provider = await session.get(ProviderUser, job.provider_id)

        applied_jobs.append({
            "application_id": application.application_id,
            "job_id": application.job_id,
            "job_title": job.title,
            "company_name": provider.username,
            "status": application.status,
            "applied_at": application.applied_at,
        })

    return applied_jobs








