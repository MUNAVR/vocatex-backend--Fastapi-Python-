from typing import Optional, List
from pydantic import BaseModel
import uuid

class ExperienceUpdate(BaseModel):
    
    company_name: Optional[str]
    duration: Optional[str]
    position: Optional[str]
    place: Optional[str]

class SkillUpdate(BaseModel):
    
    title: Optional[str]
    soft_skill: Optional[str]
    communication_skill: Optional[str]
    other_skills: Optional[str]

class EducationUpdate(BaseModel):
    
    institution_name: Optional[str]
    degree: Optional[str]
    field_of_study: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]

class ProjectUpdate(BaseModel):
    
    project_name: Optional[str]
    description: Optional[str]
    technology_used: Optional[str]
    role: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]

class AddressUpdate(BaseModel):
    street: Optional[str]
    city: Optional[str]
    state: Optional[str]
    postal_code: Optional[str]
    country: Optional[str]

class ResumeUpdate(BaseModel):
    resume_id: Optional[str]
    experiences: Optional[List[ExperienceUpdate]]
    skills: Optional[List[SkillUpdate]]
    educations: Optional[List[EducationUpdate]]
    projects: Optional[List[ProjectUpdate]]
    address: Optional[AddressUpdate]
