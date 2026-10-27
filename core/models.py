"""Pydantic models: har node ka structured output + final report."""
from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class ExtractedInfo(BaseModel):
    """Node 1 output."""
    job_title: str = Field(description="Job title, e.g. 'AI Engineer'. Use 'Not specified' if missing.")
    company_name: Optional[str] = Field(default=None, description="Company name if mentioned, else null.")
    required_experience: str = Field(description="Experience needed, e.g. '2-4 Years'. Use 'Not specified' if missing.")
    required_skills: List[str] = Field(default_factory=list, description="All skills/technologies required.")


class JobClassification(BaseModel):
    """Node 2 output."""
    job_category: str = Field(
        description="One of: Artificial Intelligence, Web Development, Data Science, Mobile Development, "
                    "DevOps/Cloud, Cybersecurity, Design, Other."
    )
    employment_type: Literal["Full-time", "Part-time", "Internship", "Contract", "Not specified"]
    work_mode: Literal["Remote", "Hybrid", "On-site", "Not specified"]


class SkillAnalysis(BaseModel):
    """Node 3 output."""
    technical_skills: List[str] = Field(default_factory=list)
    soft_skills: List[str] = Field(default_factory=list, description="e.g. Communication, Teamwork.")
    top_3_skills: List[str] = Field(description="Exactly the 3 most important skills, most important first.")


class HiringReport(BaseModel):
    """Node 4 output (final report)."""
    job_title: str
    company: str
    experience: str
    required_skills: List[str]
    job_category: str
    employment_type: str
    work_mode: str
    technical_skills: List[str]
    soft_skills: List[str]
    top_3_skills: List[str]
    summary: str
