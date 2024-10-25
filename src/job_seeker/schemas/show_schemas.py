from pydantic import BaseModel
from typing import Optional,List
from uuid import UUID
from datetime import datetime


class PersonalInfoResponse(BaseModel):
    first_name: str
    last_name: str
    position: str
    about: str

# Experience Schema
class ExperienceResponse(BaseModel):
    company_name: str
    duration: str
    position: str
    place: str


# Skill Schema
class SkillResponse(BaseModel):
    title: str
    soft_skill: str
    communication_skill: str
    other_skills: str


# Education Schema
class EducationResponse(BaseModel):
    institution_name: str
    degree: str
    field_of_study: str
    start_date: str
    end_date: str


# Project Schema
class ProjectResponse(BaseModel):
    project_name: str
    description: str
    technology_used: str
    role: str
    start_date: str
    end_date: str


# Address Schema
class AddressResponse(BaseModel):
    street: str
    city: str
    state: str
    postal_code: str
    country: str

class ResumeDetailsResponse(BaseModel):
    resume_id: UUID
    personal_info: List[PersonalInfoResponse]
    addresses: List[AddressResponse]
    skills: List[SkillResponse]
    projects: List[ProjectResponse]
    educations: List[EducationResponse]
    experiences: List[ExperienceResponse]