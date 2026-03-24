import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class RoadmapGenerateRequest(BaseModel):
    company: str
    role: str
    weeks: int
    current_skills: list[str] = []


class TopicProgressUpdate(BaseModel):
    week_number: int
    topic: str
    completed: bool


class RoadmapProgressResponse(BaseModel):
    week_number: int
    topic: str
    completed: bool
    completed_at: Optional[datetime]

    model_config = {"from_attributes": True}


class RoadmapResponse(BaseModel):
    id: uuid.UUID
    company: str
    role: str
    total_weeks: int
    current_week: int
    status: str
    weekly_plan: list
    skill_gap: dict
    created_at: datetime

    model_config = {"from_attributes": True}


class SkillGapRequest(BaseModel):
    company: str
    role: str
    user_skills: Optional[list[str]] = None  # if None, uses skills from DB


class SkillGapResponse(BaseModel):
    company: str
    role: str
    required_skills: list[str]
    missing_skills: list[dict]    # [{skill, priority}]
    existing_skills: list[str]
    recommendations: list[str]   # simple string studying steps
    match_score: float
