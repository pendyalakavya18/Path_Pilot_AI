from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from database import get_db
from models.user import User
from models.roadmap import Roadmap, RoadmapProgress
from models.test import PracticeTest
from models.interview import Interview
from services.auth_service import get_current_user

router = APIRouter()


@router.get("")
async def get_progress(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Active roadmap
    roadmap_result = await db.execute(
        select(Roadmap).where(Roadmap.user_id == current_user.id, Roadmap.status == "active")
        .order_by(Roadmap.created_at.desc()).limit(1)
    )
    roadmap = roadmap_result.scalar_one_or_none()

    roadmap_progress = 0.0
    current_week = 0
    if roadmap:
        total_result = await db.execute(
            select(func.count()).where(RoadmapProgress.roadmap_id == roadmap.id)
        )
        done_result = await db.execute(
            select(func.count()).where(
                RoadmapProgress.roadmap_id == roadmap.id,
                RoadmapProgress.completed == True,
            )
        )
        total = total_result.scalar() or 1
        done = done_result.scalar() or 0
        roadmap_progress = round((done / total) * 100, 1)
        current_week = roadmap.current_week

    # Test performance
    test_result = await db.execute(
        select(PracticeTest).where(
            PracticeTest.user_id == current_user.id,
            PracticeTest.score.isnot(None),
        ).order_by(PracticeTest.taken_at.desc()).limit(10)
    )
    tests = test_result.scalars().all()
    avg_test_score = round(sum(t.score for t in tests) / len(tests), 1) if tests else 0.0

    # Interview performance
    interview_result = await db.execute(
        select(Interview).where(
            Interview.user_id == current_user.id,
            Interview.state == "completed",
        ).order_by(Interview.created_at.desc()).limit(5)
    )
    interviews = interview_result.scalars().all()
    avg_interview_score = round(sum(i.overall_score for i in interviews if i.overall_score) / len(interviews), 1) if interviews else 0.0

    # Overall readiness
    readiness_score = (
        roadmap_progress * 0.30
        + (avg_test_score / 100) * 10 * 0.30
        + avg_interview_score * 0.40
    )
    if readiness_score >= 8:
        readiness_label = "Highly Ready"
    elif readiness_score >= 6:
        readiness_label = "Ready"
    elif readiness_score >= 4:
        readiness_label = "Moderately Ready"
    else:
        readiness_label = "Not Ready"

    test_history = [{"date": t.taken_at.strftime("%b %d"), "score": t.score} for t in reversed(tests)]
    interview_history = [{"date": i.created_at.strftime("%b %d"), "score": i.overall_score} for i in reversed(interviews)]

    return {
        "roadmap_progress_percent": roadmap_progress,
        "current_week": current_week,
        "avg_test_score": avg_test_score,
        "tests_taken": len(tests),
        "avg_interview_score": avg_interview_score,
        "interviews_taken": len(interviews),
        "overall_readiness_score": round(readiness_score, 2),
        "readiness_label": readiness_label,
        "test_history": test_history,
        "interview_history": interview_history,
    }
