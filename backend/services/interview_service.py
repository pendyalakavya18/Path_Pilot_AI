"""
interview_service.py — Interview session orchestration via InterviewAgent
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm.attributes import flag_modified

from models.interview import Interview
from models.user import User
from ai.agents.interview_agent import InterviewAgent
from config import settings


async def start_interview(
    user: User, topic: str, difficulty: str, num_questions: int, db: AsyncSession,
    company: str = None, role: str = None
) -> Interview:
    agent = InterviewAgent()
    
    # Fetch target skills from WebAgent for context awareness
    target_skills = []
    if company and role:
        from ai.agents.web_agent import web_agent
        try:
            target_skills = await web_agent.get_company_requirements(company, role)
        except Exception:
            pass

    # Generate only the first question dynamically
    generated = await agent.generate_questions(topic=topic, difficulty=difficulty, num_questions=1)
    
    # Initialize placeholders for the total duration
    questions = [{"question": "TBD", "type": "technical", "hints": [], "key_points": []} for _ in range(num_questions)]
    if generated:
        questions[0] = generated[0]

    interview = Interview(
        user_id=user.id,
        topic=topic,
        company=company,
        role=role,
        difficulty=difficulty,
        questions=questions,
        state="in_progress",
        current_question_index=0,
    )
    db.add(interview)
    await db.flush()
    return interview


async def submit_answer(
    interview_id: str,
    answer: str,
    db: AsyncSession,
) -> dict:
    result = await db.execute(select(Interview).where(Interview.id == interview_id))
    interview = result.scalar_one_or_none()
    if not interview:
        raise ValueError("Interview not found")

    agent = InterviewAgent()
    current_q = interview.questions[interview.current_question_index]

    # Evaluate this answer
    evaluation = await agent.evaluate_answer(question=current_q["question"], answer=answer)
    evaluation["question"] = current_q["question"]
    evaluation["answer"] = answer

    # Append evaluation
    evals = list(interview.evaluations or [])
    evals.append(evaluation)
    interview.evaluations = evals
    flag_modified(interview, "evaluations")

    # Check if we need a follow-up
    needs_followup = evaluation.get("overall_score", 5) < 6.0
    follow_up = None
    if needs_followup:
        follow_up = await agent.generate_follow_up(current_q["question"], answer)

    # Advance question index (skip if follow-up)
    if not needs_followup or len([e for e in evals if e["question"] == current_q["question"]]) >= 2:
        interview.current_question_index += 1

    is_complete = interview.current_question_index >= len(interview.questions)
    
    # If not complete, we must generate the next question if it's currently a TBD placeholder
    if not is_complete and not follow_up:
        nxt_idx = interview.current_question_index
        q_list = list(interview.questions)
        if q_list[nxt_idx]["question"] == "TBD":
            # Pass company/role context (target_skills) to next question generator
            target_skills = []
            if interview.company and interview.role:
                from ai.agents.web_agent import web_agent
                target_skills = await web_agent.get_company_requirements(interview.company, interview.role)

            next_generated = await agent.generate_next_question(
                interview.topic, interview.difficulty, evals, target_skills=target_skills
            )
            q_list[nxt_idx] = next_generated
            interview.questions = q_list
            flag_modified(interview, "questions")

    if is_complete:
        # Generate final summary
        summary = await agent.generate_summary(evals)
        interview.overall_score = summary["overall_score"]
        interview.technical_score = summary["technical_score"]
        interview.communication_score = summary["communication_score"]
        interview.confidence_score = summary["confidence_score"]
        interview.feedback = summary["feedback"]
        interview.strengths = summary["strengths"]
        interview.improvements = summary["improvements"]
        interview.state = "completed"

    next_question = None
    if not is_complete:
        if follow_up:
            next_question = follow_up
        else:
            nq = interview.questions[interview.current_question_index]
            next_question = nq["question"]

    return {
        "is_complete": is_complete,
        "evaluation": evaluation,
        "next_question": next_question,
        "question_index": interview.current_question_index,
        "total_questions": len(interview.questions),
    }
