from sqlmodel import SQLModel, Field, Column, Relationship
from datetime import datetime
import uuid
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import ForeignKey,LargeBinary
from typing import Optional

class JobApplication(SQLModel, table=True):
    __tablename__ = "JobApplication"
    application_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, default=uuid.uuid4)
    )
    user_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, ForeignKey("User.uid"), nullable=False)
    )
    job_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, ForeignKey("JobDetails.job_id"), nullable=False)
    )
    resume_file: Optional[bytes] = Field(
        sa_column=Column(LargeBinary, nullable=True)
    ) 
    status: str = Field(default="pending") 
    applied_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now)
    )

    # Relationships
    applicant: "User" = Relationship(back_populates="applications")
    job: "JobDetails" = Relationship()

    def __repr__(self):
        return f"<JobApplication {self.application_id} by {self.user_id} for job {self.job_id}>"
