import uuid
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from sqlalchemy import Column, ForeignKey
import sqlalchemy.dialects.postgresql as pg


class ResumeDetails(SQLModel, table=True):
    __tablename__ = "resume_details"
    
    resume_id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False, 
            primary_key=True,
            default=uuid.uuid4  
        )
    )

    user_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, ForeignKey("User.uid", ondelete="CASCADE"), nullable=False, unique=True)
    )

    experiences: List["Experience"] = Relationship(
        back_populates="resume", 
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    skills: List["Skill"] = Relationship(
        back_populates="resume", 
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    educations: List["Education"] = Relationship(
        back_populates="resume", 
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    projects: List["Project"] = Relationship(
        back_populates="resume", 
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    
    address: Optional["Address"] = Relationship(
        back_populates="resume", 
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    
    personal_info: Optional["PersonalInfo"] = Relationship(
        back_populates="resume", 
        sa_relationship_kwargs={"lazy": "selectin"}
    )


class Experience(SQLModel, table=True):
    __tablename__ = "experience"
    
    experience_id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False, 
            primary_key=True,
            default=uuid.uuid4  
        )
    )
    company_name: str
    duration: str
    position: str
    place: str
    resume_id: uuid.UUID = Field(foreign_key="resume_details.resume_id")
    resume: Optional[ResumeDetails] = Relationship(
        back_populates="experiences", 
        sa_relationship_kwargs={"lazy": "selectin"}
    )


class Skill(SQLModel, table=True):
    __tablename__ = "skills"
    
    skill_id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False, 
            primary_key=True,
            default=uuid.uuid4  
        )
    )
    title: str
    soft_skill: str
    communication_skill: str
    other_skills: str
    resume_id: uuid.UUID = Field(foreign_key="resume_details.resume_id")
    resume: Optional[ResumeDetails] = Relationship(
        back_populates="skills", 
        sa_relationship_kwargs={"lazy": "selectin"}
    )


class Education(SQLModel, table=True):
    __tablename__ = "education"
    
    education_id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False, 
            primary_key=True,
            default=uuid.uuid4  
        )
    )
    institution_name: str
    degree: str
    field_of_study: str
    start_date: str
    end_date: str
    resume_id: uuid.UUID = Field(foreign_key="resume_details.resume_id")
    resume: Optional[ResumeDetails] = Relationship(
        back_populates="educations", 
        sa_relationship_kwargs={"lazy": "selectin"}
    )


class Project(SQLModel, table=True):
    __tablename__ = "projects"
    
    project_id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False, 
            primary_key=True,
            default=uuid.uuid4  
        )
    )
    project_name: str
    description: str
    technology_used: str
    role: str
    start_date: str
    end_date: str
    resume_id: uuid.UUID = Field(foreign_key="resume_details.resume_id")
    resume: Optional[ResumeDetails] = Relationship(
        back_populates="projects", 
        sa_relationship_kwargs={"lazy": "selectin"}
    )


class Address(SQLModel, table=True):
    __tablename__ = "address"
    
    address_id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False, 
            primary_key=True,
            default=uuid.uuid4  
        )
    )
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    resume_id: uuid.UUID = Field(foreign_key="resume_details.resume_id")
    resume: Optional[ResumeDetails] = Relationship(
        back_populates="address", 
        sa_relationship_kwargs={"lazy": "selectin"}
    )


class PersonalInfo(SQLModel, table=True):
    __tablename__ = "personal_info"
    
    personal_info_id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False, 
            primary_key=True,
            default=uuid.uuid4  
        )
    )
    first_name: str
    last_name: str
    position: str
    about: str
    resume_id: uuid.UUID = Field(foreign_key="resume_details.resume_id")
    resume: Optional[ResumeDetails] = Relationship(
        back_populates="personal_info", 
        sa_relationship_kwargs={"lazy": "selectin"}
    )
