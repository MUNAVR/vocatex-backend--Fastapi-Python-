
from sqlalchemy.ext.asyncio import AsyncSession
from src.job_seeker.dependancies import *
from src.job_seeker.schemas.create_schemas import *
from src.job_seeker.schemas.show_schemas import *
from src.job_seeker.models import *
from src.auth.models  import *
from src.job_seeker.schemas.edit_schemas import *
from sqlalchemy import select

# Sample code to populate related data
async def get_related_data(resume_id: UUID, session: AsyncSession):
    addresses_query = select(Address).where(Address.resume_id == resume_id)
    addresses_result = await session.execute(addresses_query)
    addresses = addresses_result.scalars().all()

    skills_query = select(Skill).where(Skill.resume_id == resume_id)
    skills_result = await session.execute(skills_query)
    skills = skills_result.scalars().all()

    projects_query = select(Project).where(Project.resume_id == resume_id)
    projects_result = await session.execute(projects_query)
    projects = projects_result.scalars().all()

    educations_query = select(Education).where(Education.resume_id == resume_id)
    educations_result = await session.execute(educations_query)
    educations = educations_result.scalars().all()

    experiences_query = select(Experience).where(Experience.resume_id == resume_id)
    experiences_result = await session.execute(experiences_query)
    experiences = experiences_result.scalars().all()

    return {
        "addresses": addresses,
        "skills": skills,
        "projects": projects,
        "educations": educations,
        "experiences": experiences,
    }
