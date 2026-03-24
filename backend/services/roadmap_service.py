"""
roadmap_service.py — Roadmap generation, enrichment, and adaptation
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime

from models.roadmap import Roadmap, RoadmapProgress
from models.user import User
from ai.llm_engine import llm_engine
from ai.rag_pipeline import rag_pipeline
from ai.agents.roadmap_agent import RoadmapAgent
from ai.agents.skill_agent import SkillAgent


async def generate_roadmap(
    user: User,
    company: str,
    role: str,
    weeks: int,
    current_skills: list[str],
    db: AsyncSession,
) -> Roadmap:
    # 1. Run skill gap analysis to prioritize topics
    skill_agent = SkillAgent()
    gap_result = await skill_agent.analyze(
        user_skills=current_skills,
        company=company,
        role=role,
    )

    # 2. Retrieve relevant resources via RAG
    context_docs = await rag_pipeline.search(
        query=f"{role} at {company} roadmap preparation",
        collection="learning_resources",
        top_k=10,
    )

    # 3. Generate week-by-week plan with LLM
    weekly_plan = await llm_engine.generate_roadmap(
        role=role,
        company=company,
        weeks=weeks,
        current_skills=current_skills,
        required_skills=gap_result.get("required_skills", []),
        missing_skills=[s["skill"] for s in gap_result.get("missing_skills", [])],
        context=context_docs,
    )

    # 4. Enrich each day's topic with learning resources
    for week in weekly_plan:
        enriched_days = []
        for day_obj in week.get("days", []):
            topic = day_obj.get("topic", "")
            if not topic: continue
            resources = await rag_pipeline.search(
                query=topic,
                collection="learning_resources",
                top_k=3,
            )
            # Create enriched day struct
            enriched_days.append({
                "day": day_obj.get("day"),
                "topic": topic,
                "resources": resources
            })
        week["days"] = enriched_days

    # 5. Persist to database
    roadmap = Roadmap(
        user_id=user.id,
        company=company,
        role=role,
        total_weeks=weeks,
        weekly_plan=weekly_plan,
        skill_gap=gap_result,
    )
    db.add(roadmap)
    await db.flush()

    # 6. Seed progress tracker rows
    for week in weekly_plan:
        wk_num = week.get("week", 0)
        for day_obj in week.get("days", []):
            topic = day_obj.get("topic", "")
            if topic:
                db.add(RoadmapProgress(roadmap_id=roadmap.id, week_number=wk_num, topic=topic))

    return roadmap


async def mark_topic_complete(
    roadmap_id: str,
    week_number: int,
    topic: str,
    completed: bool,
    db: AsyncSession,
) -> RoadmapProgress:
    result = await db.execute(
        select(RoadmapProgress).where(
            RoadmapProgress.roadmap_id == roadmap_id,
            RoadmapProgress.week_number == week_number,
            RoadmapProgress.topic == topic,
        )
    )
    progress = result.scalar_one_or_none()
    if not progress:
        raise ValueError("Topic not found in roadmap")

    progress.completed = completed
    progress.completed_at = datetime.utcnow() if completed else None

    # Update roadmap current_week if needed
    if completed:
        roadmap_result = await db.execute(select(Roadmap).where(Roadmap.id == roadmap_id))
        roadmap = roadmap_result.scalar_one_or_none()
        if roadmap and week_number > roadmap.current_week:
            roadmap.current_week = week_number

    return progress


async def adapt_roadmap(roadmap_id: str, db: AsyncSession) -> Roadmap:
    result = await db.execute(select(Roadmap).where(Roadmap.id == roadmap_id))
    roadmap = result.scalar_one_or_none()
    if not roadmap:
        raise ValueError("Roadmap not found")

    agent = RoadmapAgent()
    adapted_plan = await agent.adapt(roadmap)
    roadmap.weekly_plan = adapted_plan
    roadmap.updated_at = datetime.utcnow()
    return roadmap
