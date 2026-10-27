"""Shared LangGraph state - nodes ke beech data isi se pass hota hai."""
from typing import Optional, TypedDict

from core.models import ExtractedInfo, JobClassification, SkillAnalysis, HiringReport


class GraphState(TypedDict, total=False):
    job_description: str
    extracted: Optional[ExtractedInfo]
    classification: Optional[JobClassification]
    skills: Optional[SkillAnalysis]
    report: Optional[HiringReport]
    error: Optional[str]
