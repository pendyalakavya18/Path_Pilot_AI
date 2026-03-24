from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class SkillItem(BaseModel):
    skill_name: str
    proficiency: str = "beginner"  # beginner | intermediate | advanced


class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    cgpa: Optional[float] = None
    branch: Optional[str] = None
    graduation_year: Optional[int] = None
    experience_years: Optional[float] = None
    target_company: Optional[str] = None
    target_role: Optional[str] = None


class UserSkillsUpdate(BaseModel):
    skills: list[SkillItem]


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    cgpa: Optional[float]
    branch: Optional[str]
    graduation_year: Optional[int]
    experience_years: float
    target_company: Optional[str]
    target_role: Optional[str]
    skills: list[SkillItem] = []
    created_at: datetime

    model_config = {"from_attributes": True}
