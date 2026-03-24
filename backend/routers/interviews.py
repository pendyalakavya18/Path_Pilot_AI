import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models.user import User
from models.interview import Interview
from schemas.interview import (
    InterviewStartRequest, InterviewAnswerRequest,
    InterviewNextResponse, InterviewSummaryResponse, EvaluationResult,
)
from services.auth_service import get_current_user
from services.interview_service import start_interview, submit_answer

router = APIRouter()


@router.post("/start", status_code=201)
async def start(
    payload: InterviewStartRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    company = payload.company or current_user.target_company
    role = payload.role or current_user.target_role

    interview = await start_interview(
        user=current_user,
        topic=payload.topic,
        difficulty=payload.difficulty,
        num_questions=payload.num_questions,
        company=company,
        role=role,
        db=db,
    )
    first_question = interview.questions[0]["question"] if interview.questions else ""
    return {
        "interview_id": str(interview.id),
        "question": first_question,
        "question_index": 0,
        "total_questions": len(interview.questions),
        "is_complete": False,
    }


@router.post("/{interview_id}/answer")
async def answer(
    interview_id: uuid.UUID,
    payload: InterviewAnswerRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Verify ownership
    result = await db.execute(
        select(Interview).where(Interview.id == str(interview_id), Interview.user_id == current_user.id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Interview not found")

    response = await submit_answer(str(interview_id), payload.answer, db)
    return response


@router.get("/{interview_id}/summary", response_model=InterviewSummaryResponse)
async def get_summary(
    interview_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Interview).where(Interview.id == str(interview_id), Interview.user_id == current_user.id)
    )
    interview = result.scalar_one_or_none()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    if interview.state != "completed":
        raise HTTPException(status_code=400, detail="Interview not yet completed")
    return interview


@router.get("", response_model=list[InterviewSummaryResponse])
async def list_interviews(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Interview)
        .where(Interview.user_id == current_user.id, Interview.state == "completed")
        .order_by(Interview.created_at.desc())
    )
    return result.scalars().all()
