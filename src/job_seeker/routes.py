from fastapi import APIRouter, Depends, HTTPException,status,Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID,uuid4
from src.db.main import get_session
from src.job_seeker.dependancies import *
from src.job_seeker.schemas.create_schemas import *
from src.job_seeker.schemas.show_schemas import *
from src.job_seeker.models import *
from src.auth.models  import *
from src.job_seeker.schemas.edit_schemas import *
from sqlalchemy import select
from src.job_seeker.service import *
from sqlalchemy.orm import selectinload



resume_router=APIRouter()
access_token_bearer=AccessTokenBearer()


class ResumeStep1(BaseModel):
    personalinfp:list[PersonalInfoCreate]

class ResumeStep2(BaseModel):
    address: List[AddressCreate]

class ResumeStep3(BaseModel):
    skills: List[SkillCreate]
    
class ResumeStep4(BaseModel):
    projects: List[Project]

class ResumeStep5(BaseModel):
    educations: List[Education]

class ResumeStep6(BaseModel):
    experiences: List[Experience]



@resume_router.post("/resume/step1/")
async def create_personal_info(
    resume_step1: ResumeStep1, 
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer)
):
    user_id = user_details['user']['user_uid']
    
    
    existing_resume = await session.execute(
        select(ResumeDetails).where(ResumeDetails.user_id == user_id)
    )
    if existing_resume.scalars().first():
        return {"message": "User already has a resume. Please update the existing resume."}

    resume_id = uuid4()
    
    
    resume = ResumeDetails(
        resume_id=resume_id,
        user_id=user_id
    )
    session.add(resume)

    
    for personal_info in resume_step1.personalinfp:
        personal = PersonalInfo(
            first_name=personal_info.first_name,
            last_name=personal_info.last_name, 
            position=personal_info.position,
            about=personal_info.about,
            resume_id=resume_id  
        )
        session.add(personal)
    
    
    await session.commit()
    await session.refresh(resume)

    return {"resume_id": resume_id}




# Endpoint for Step 2: Address
@resume_router.post("/resume/step2/{resume_id}")
async def add_address(
    resume_id: UUID, 
    resume_step2: ResumeStep2, 
    session: AsyncSession = Depends(get_session)
):
    query = select(ResumeDetails).where(ResumeDetails.resume_id == resume_id)
    result = await session.execute(query)
    resume = result.scalar()

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    for address in resume_step2.address:
        address_obj = Address(**address.dict(), resume_id=resume_id)
        session.add(address_obj)

    await session.commit()
    return {"message": "Addresses added successfully"}


@resume_router.post("/resume/step3/{resume_id}")
async def add_skills(
    resume_id: UUID, 
    resume_step3: ResumeStep3, 
    session: AsyncSession = Depends(get_session)
):
    query = select(ResumeDetails).where(ResumeDetails.resume_id == resume_id)
    result = await session.execute(query)
    resume = result.scalar()

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    for skill_create in resume_step3.skills:
        skill = Skill(
            title=skill_create.title,  
            soft_skill=skill_create.soft_skill,  
            communication_skill=skill_create.communication_skill,  
            other_skills=skill_create.other_skills,  
            resume_id=resume_id
        )
        session.add(skill)

    await session.commit()
    return {"message": "Skills added successfully"}



@resume_router.post("/resume/step4/{resume_id}")
async def add_projects(
    resume_id: UUID, 
    resume_step4: ResumeStep4, 
    session: AsyncSession = Depends(get_session)
):
    # Fetch the resume to ensure it exists
    query = select(ResumeDetails).where(ResumeDetails.resume_id == resume_id)
    result = await session.execute(query)
    resume = result.scalar()

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    for project in resume_step4.projects:
        # Exclude project_id and resume_id from project data
        project_data = project.dict(exclude={"project_id", "resume_id"})  # Exclude both IDs
        
        # Create a new Project object and set resume_id
        project_obj = Project(
            project_id=uuid4(),  # Generate a new UUID for each project
            resume_id=resume_id,  # Set the resume_id here
            **project_data  # Unpack the rest of the project data
        )

        # Check for duplicate project names within the same resume
        existing_project = await session.execute(
            select(Project).where(Project.project_name == project.project_name, Project.resume_id == resume_id)
        )
        
        if existing_project.scalars().first():
            raise HTTPException(status_code=400, detail=f"Project '{project.project_name}' already exists for this resume.")

        session.add(project_obj)

    # Commit the session to save all new projects
    await session.commit()
    
    return {"message": "Projects added successfully"}



# Endpoint for Step 5: Education

@resume_router.post("/resume/step5/{resume_id}")
async def add_education(
    resume_id: UUID, 
    resume_step5: ResumeStep5, 
    session: AsyncSession = Depends(get_session)
):
    # Fetch the resume to ensure it exists
    query = select(ResumeDetails).where(ResumeDetails.resume_id == resume_id)
    result = await session.execute(query)
    resume = result.scalar()

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    for education in resume_step5.educations:
        # Unpack the dictionary and exclude 'resume_id' and 'education_id' if it's included
        education_data = education.dict(exclude={"resume_id", "education_id"})  # Exclude both

        # Create a new Education object and set a new UUID for education_id
        education_obj = Education(
            education_id=uuid4(),  # Generate a new UUID for each education entry
            resume_id=resume_id,    # Set the resume_id here
            **education_data        # Unpack the rest of the education data
        )
        
        session.add(education_obj)

    # Commit the session to save all new education entries
    await session.commit()
    
    return {"message": "Education added successfully"}




# Endpoint for Step 6: Experiences
@resume_router.post("/resume/step6/{resume_id}")  # Replace stepX with the appropriate step number for experience
async def add_experience(
    resume_id: UUID, 
    resume_stepX: ResumeStep6,  # Update this to your actual data model
    session: AsyncSession = Depends(get_session)
):
    # Fetch the resume to ensure it exists
    query = select(ResumeDetails).where(ResumeDetails.resume_id == resume_id)
    result = await session.execute(query)
    resume = result.scalar()

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    for experience in resume_stepX.experiences:  # Ensure you're iterating over the correct field
        # Unpack the dictionary and exclude 'resume_id' and 'experience_id' if included
        experience_data = experience.dict(exclude={"resume_id", "experience_id"})  # Exclude both

        # Create a new Experience object with a new UUID for experience_id
        experience_obj = Experience(
            experience_id=uuid4(),  # Generate a new UUID for each experience entry
            resume_id=resume_id,     # Set the resume_id here
            **experience_data        # Unpack the rest of the experience data
        )
        
        session.add(experience_obj)

    # Commit the session to save all new experience entries
    await session.commit()
    
    return {"message": "Experience added successfully"}



@resume_router.get("/get_resume/", response_model=ResumeDetailsResponse)
async def get_resume(session: AsyncSession = Depends(get_session),
                     user_details=Depends(access_token_bearer)):
    
    user_id = user_details['user']['user_uid']
    print(user_id)
    
    # Execute the query to fetch resume details
    result = await session.execute(
        select(ResumeDetails).where(ResumeDetails.user_id == user_id)
    )
    
    # Extract the first result
    existing_resume = result.scalar_one_or_none()
    
    # Check if no resume is found
    if not existing_resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    resume_id = existing_resume.resume_id
    print(resume_id)

    # Query the ResumeDetails based on resume_id, with a join to PersonalInfo
    query = (
        select(ResumeDetails)
        .options(selectinload(ResumeDetails.personal_info))  # Assuming relationship exists
        .where(ResumeDetails.resume_id == resume_id)
    )
    result = await session.execute(query)
    resume = result.scalar_one_or_none()

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    # Retrieve related data
    related_data = await get_related_data(resume_id, session)

    # Constructing the response
    response_data = ResumeDetailsResponse(
        resume_id=resume.resume_id,
        personal_info=[
            PersonalInfoResponse(
                first_name=resume.personal_info.first_name,  # Make sure `first_name` exists
                last_name=resume.personal_info.last_name,    # Make sure `last_name` exists
                position=resume.personal_info.position,
                about=resume.personal_info.about
            )
        ],
        addresses=[AddressResponse(**addr.dict()) for addr in related_data['addresses']],
        skills=[SkillResponse(**skill.dict()) for skill in related_data['skills']],
        projects=[ProjectResponse(**proj.dict()) for proj in related_data['projects']],
        educations=[EducationResponse(**edu.dict()) for edu in related_data['educations']],
        experiences=[ExperienceResponse(**exp.dict()) for exp in related_data['experiences']],
    )

    return response_data

  




   