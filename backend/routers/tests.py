import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models.user import User
from models.test import PracticeTest
from schemas.test import TestGenerateRequest, TestSubmitRequest, TestResultResponse
from services.auth_service import get_current_user
from services.test_service import generate_test, evaluate_test

router = APIRouter()


@router.post("/generate", status_code=201)
async def create_test(
    payload: TestGenerateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    test = await generate_test(
        user=current_user,
        topic=payload.topic,
        num_questions=payload.num_questions,
        roadmap_id=payload.roadmap_id,
        db=db,
    )
    return {
        "test_id": str(test.id),
        "topic": test.topic,
        "total_questions": test.total_questions,
        "questions": [
            {"index": i, "question": q["question"], "options": q.get("options", [])}
            for i, q in enumerate(test.questions)
        ],
    }


@router.post("/submit")
async def submit_test(
    payload: TestSubmitRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Verify ownership
    result = await db.execute(
        select(PracticeTest).where(PracticeTest.id == str(payload.test_id), PracticeTest.user_id == current_user.id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Test not found")

    return await evaluate_test(str(payload.test_id), payload.answers, db)


@router.get("", response_model=list[TestResultResponse])
async def list_tests(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(PracticeTest)
        .where(PracticeTest.user_id == current_user.id, PracticeTest.score.isnot(None))
        .order_by(PracticeTest.taken_at.desc())
    )
    return result.scalars().all()
