from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional

from models.user import User
from services.auth_service import get_current_user
from services.eligibility_service import check_eligibility, get_eligible_companies

router = APIRouter()


class EligibilityCheckRequest(BaseModel):
    company: str
    cgpa: Optional[float] = None
    branch: Optional[str] = None
    experience_years: Optional[float] = None
    skills: Optional[list[str]] = None


@router.post("/check")
async def check(
    payload: EligibilityCheckRequest,
    current_user: User = Depends(get_current_user),
):
    cgpa = payload.cgpa if payload.cgpa is not None else (current_user.cgpa or 0.0)
    branch = payload.branch or current_user.branch or ""
    experience = payload.experience_years if payload.experience_years is not None else current_user.experience_years
    skills = payload.skills or [s.skill_name for s in current_user.skills]

    return check_eligibility(
        company=payload.company,
        user_cgpa=cgpa,
        user_branch=branch,
        user_experience=experience,
        user_skills=skills,
    )


@router.get("/suggestions")
async def suggestions(current_user: User = Depends(get_current_user)):
    skills = [s.skill_name for s in current_user.skills]
    return get_eligible_companies(
        user_cgpa=current_user.cgpa or 0.0,
        user_branch=current_user.branch or "",
        user_experience=current_user.experience_years,
        user_skills=skills,
    )
