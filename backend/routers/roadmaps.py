import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models.user import User
from models.roadmap import Roadmap, RoadmapProgress
from schemas.roadmap import (
    RoadmapGenerateRequest, RoadmapResponse,
    TopicProgressUpdate, SkillGapRequest, SkillGapResponse,
)
from services.auth_service import get_current_user
from services.roadmap_service import generate_roadmap, mark_topic_complete, adapt_roadmap
from ai.agents.skill_agent import SkillAgent

router = APIRouter()


@router.post("/generate", response_model=RoadmapResponse, status_code=201)
async def create_roadmap(
    payload: RoadmapGenerateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from config import settings
    weeks = max(settings.MIN_ROADMAP_WEEKS, min(payload.weeks, settings.MAX_ROADMAP_WEEKS))
    user_skills = payload.current_skills or [s.skill_name for s in current_user.skills]

    roadmap = await generate_roadmap(
        user=current_user,
        company=payload.company,
        role=payload.role,
        weeks=weeks,
        current_skills=user_skills,
        db=db,
    )
    return roadmap


@router.get("", response_model=list[RoadmapResponse])
async def list_roadmaps(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Roadmap).where(Roadmap.user_id == current_user.id).order_by(Roadmap.created_at.desc())
    )
    return result.scalars().all()


@router.get("/{roadmap_id}", response_model=RoadmapResponse)
async def get_roadmap(
    roadmap_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Roadmap).where(Roadmap.id == roadmap_id, Roadmap.user_id == current_user.id)
    )
    roadmap = result.scalar_one_or_none()
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    return roadmap


@router.put("/{roadmap_id}/progress")
async def update_progress(
    roadmap_id: str,
    payload: TopicProgressUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Verify ownership
    result = await db.execute(
        select(Roadmap).where(Roadmap.id == roadmap_id, Roadmap.user_id == current_user.id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Roadmap not found")

    progress = await mark_topic_complete(
        roadmap_id=str(roadmap_id),
        week_number=payload.week_number,
        topic=payload.topic,
        completed=payload.completed,
        db=db,
    )
    return {"week_number": progress.week_number, "topic": progress.topic, "completed": progress.completed}


@router.post("/{roadmap_id}/adapt")
async def trigger_adaptation(
    roadmap_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Roadmap).where(Roadmap.id == roadmap_id, Roadmap.user_id == current_user.id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Roadmap not found")

    roadmap = await adapt_roadmap(str(roadmap_id), db)
    return {"adapted": True, "total_weeks": roadmap.total_weeks}


@router.post("/skill-gap", response_model=SkillGapResponse)
async def analyze_skill_gap(
    payload: SkillGapRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from models.roadmap import SkillGapAnalysis
    skills = payload.user_skills or [s.skill_name for s in current_user.skills]
    agent = SkillAgent()
    gap = await agent.analyze(user_skills=skills, company=payload.company, role=payload.role)
    
    # Persist the analysis result
    analysis = SkillGapAnalysis(
        user_id=current_user.id,
        company=payload.company,
        role=payload.role,
        required_skills=gap.get("required_skills", []),
        user_skills=gap.get("user_skills", []),
        missing_skills=gap.get("missing_skills", []),
        existing_skills=gap.get("existing_skills", []),
        recommendations=gap.get("recommendations", []),
        match_score=gap.get("match_score", 0.0),
    )
    db.add(analysis)
    await db.flush()
    
    return SkillGapResponse(**gap)
