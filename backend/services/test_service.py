"""
test_service.py — Practice test generation and scoring
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.test import PracticeTest
from models.user import User
from ai.llm_engine import llm_engine
from ai.rag_pipeline import rag_pipeline


async def generate_test(
    user: User,
    topic: str,
    num_questions: int,
    roadmap_id,
    db: AsyncSession,
) -> PracticeTest:
    # Retrieve topic context from RAG
    context = await rag_pipeline.search(query=topic, collection="learning_resources", top_k=5)

    # Generate questions via LLM
    questions = await llm_engine.generate_practice_test(
        topic=topic,
        num_questions=num_questions,
        context=context,
    )

    test = PracticeTest(
        user_id=user.id,
        roadmap_id=roadmap_id,
        topic=topic,
        questions=questions,
        total_questions=len(questions),
    )
    db.add(test)
    await db.flush()
    return test


def _performance_level(score: float) -> str:
    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Average"
    return "Needs Improvement"


async def evaluate_test(test_id: str, answers: list[int], db: AsyncSession) -> dict:
    result = await db.execute(select(PracticeTest).where(PracticeTest.id == test_id))
    test = result.scalar_one_or_none()
    if not test:
        raise ValueError("Test not found")

    questions = test.questions
    if len(answers) != len(questions):
        raise ValueError("Answer count does not match question count")

    correct = 0
    breakdown = []
    for i, (q, user_ans) in enumerate(zip(questions, answers)):
        is_correct = user_ans == q.get("correct_answer", -1)
        if is_correct:
            correct += 1
        breakdown.append({
            "question": q.get("question", ""),
            "options": q.get("options", []),
            "correct_answer": q.get("correct_answer"),
            "user_answer": user_ans,
            "is_correct": is_correct,
            "explanation": q.get("explanation", ""),
        })

    score = round((correct / len(questions)) * 100, 2) if questions else 0.0

    test.user_answers = answers
    test.score = score
    test.performance_level = _performance_level(score)
    
    from sqlalchemy.orm.attributes import flag_modified
    flag_modified(test, "user_answers")

    return {
        "test_id": str(test.id),
        "topic": test.topic,
        "score": score,
        "total_questions": len(questions),
        "correct": correct,
        "performance_level": test.performance_level,
        "results": breakdown,
    }
