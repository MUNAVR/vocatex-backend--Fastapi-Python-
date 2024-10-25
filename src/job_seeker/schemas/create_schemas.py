from pydantic import BaseModel
from typing import Optional,List
from uuid import UUID
from datetime import datetime


class PersonalInfoCreate(BaseModel):
    first_name: str
    last_name: str
    position: str
    about: str

# Experience Schema
class ExperienceCreate(BaseModel):
    company_name: str
    duration: str
    position: str
    place: str


# Skill Schema
class SkillCreate(BaseModel):
    title: str
    soft_skill: str
    communication_skill: str
    other_skills: str


# Education Schema
class EducationCreate(BaseModel):
    institution_name: str
    degree: str
    field_of_study: str
    start_date: str
    end_date: str


# Project Schema
class ProjectCreate(BaseModel):
    project_name: str
    description: str
    technology_used: str
    role: str
    start_date: str
    end_date: str


# Address Schema
class AddressCreate(BaseModel):
    street: str
    city: str
    state: str
    postal_code: str
    country: str






