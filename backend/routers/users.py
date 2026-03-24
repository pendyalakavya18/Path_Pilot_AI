from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload

from database import get_db
from models.user import User, UserSkill
from schemas.user import UserResponse, UserProfileUpdate, UserSkillsUpdate, SkillItem
from services.auth_service import get_current_user

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_profile(
    payload: UserProfileUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(current_user, field, value)
    current_user.updated_at = datetime.utcnow()
    await db.commit()
    result = await db.execute(select(User).where(User.id == current_user.id).options(selectinload(User.skills)))
    return result.scalar_one()


@router.put("/me/skills", response_model=UserResponse)
async def update_skills(
    payload: UserSkillsUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Replace all existing skills
    await db.execute(delete(UserSkill).where(UserSkill.user_id == current_user.id))
    for item in payload.skills:
        db.add(UserSkill(user_id=current_user.id, skill_name=item.skill_name, proficiency=item.proficiency))
    await db.commit()
    await db.refresh(current_user)
    return current_user
