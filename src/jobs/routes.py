from fastapi import APIRouter, Depends, HTTPException,status,Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import List
from uuid import UUID
from src.db.main import get_session
from src.jobs.models import *
from src.jobs.schemas import *
from src.jobs.dependancies import AccessTokenBearer

jobs_router = APIRouter()
access_token_bearer = AccessTokenBearer()


# -----------------------------------------------------------------------------------


# POST: Create a new job
@jobs_router.post("/create_jobs/", response_model=JobRead, status_code=status.HTTP_201_CREATED)
async def create_job(
    job: JobCreate, session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer)
    ):
    
    print(user_details)
    new_job = JobDetails(
        title = job.title,
        description = job.description,
        salary_from = job.salary_from,  
        salary_to = job.salary_to,      
        job_type = job.job_type,
        job_mode = job.job_mode,       
        job_location = job.job_location,  
        experience = job.experience,    
        skills_and_requirements = job.skills_and_requirements, 
        provider_id = user_details['user']['user_uid']  
    )
    
    session.add(new_job)
    await session.commit()
    await session.refresh(new_job)
    
    return new_job

@jobs_router.get("/search", response_model=List[JobRead])
async def search_jobs(
    title: str = None, 
    location: str = None, 
    session: AsyncSession = Depends(get_session)
):
    query = select(JobDetails)

    if title:
        query = query.where(JobDetails.title.ilike(f"%{title}%"))
    if location:
        query = query.where(JobDetails.job_location.ilike(f"%{location}%"))

    result = await session.execute(query)
    jobs = result.scalars().all()

    if not jobs:
        raise HTTPException(status_code=404, detail="No jobs found")

    print(jobs)

    return jobs


# GET: Retrieve all jobs
@jobs_router.get("/all_jobs/", response_model=List[JobRead])
async def get_jobs(session: AsyncSession = Depends(get_session),
                   user_details=Depends(access_token_bearer)):
    result = await session.execute(select(JobDetails))
    jobs = result.scalars().all()
    return jobs


@jobs_router.get("/get_jobs/{job_id}", response_model=JobRead)
async def get_job(job_id: UUID, session: AsyncSession = Depends(get_session),
                  user_details=Depends(access_token_bearer)):
    job = await session.get(JobDetails, job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job


@jobs_router.get("/get_jobs_provider/", response_model=List[JobRead])
async def get_jobs_by_provider(session: AsyncSession = Depends(get_session),
                               user_details=Depends(access_token_bearer)):
    # Query to select all jobs where the provider_id matches
    result = await session.execute(select(JobDetails).where(JobDetails.provider_id == user_details['user']['user_uid']))
    jobs = result.scalars().all()

    if not jobs:
        raise HTTPException(status_code=404, detail="No jobs found for this provider")

    return jobs


@jobs_router.put("/edit_job/{job_id}", response_model=JobRead, status_code=status.HTTP_200_OK)
async def edit_job(job_id: UUID, job_update: JobUpdate, session: AsyncSession = Depends(get_session),
                   user_details=Depends(access_token_bearer)):
  
    job = await session.get(JobDetails, job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job_update.title:
        job.title = job_update.title
    if job_update.description:
        job.description = job_update.description
    if job_update.salary_from:
        job.salary_from = job_update.salary_from  
    if job_update.salary_to:
        job.salary_to = job_update.salary_to     
    if job_update.job_type:
        job.job_type = job_update.job_type        
    if job_update.job_location:
        job.job_location = job_update.job_location  
    if job_update.experience:
        job.experience = job_update.experience    
    if job_update.skills_and_requirements:
        job.skills_and_requirements = job_update.skills_and_requirements  

    session.add(job)
    await session.commit()
    await session.refresh(job)
    
    return job


