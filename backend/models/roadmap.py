import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Boolean, Text, DateTime, ForeignKey, Enum, Float, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class Roadmap(Base):
    __tablename__ = "roadmaps"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    company: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(100), nullable=False)
    total_weeks: Mapped[int] = mapped_column(Integer, nullable=False)
    current_week: Mapped[int] = mapped_column(Integer, default=0)

    status: Mapped[str] = mapped_column(
        Enum("active", "completed", "paused", name="roadmap_status_enum", native_enum=False),
        default="active",
    )

    # Full AI-generated week-by-week plan stored as JSON
    weekly_plan: Mapped[list] = mapped_column(JSON, default=list)
    # Skill gap at time of roadmap creation
    skill_gap: Mapped[dict] = mapped_column(JSON, default=dict)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="roadmaps")
    progress_items: Mapped[list["RoadmapProgress"]] = relationship(
        "RoadmapProgress", back_populates="roadmap", cascade="all, delete-orphan"
    )
    tests: Mapped[list["PracticeTest"]] = relationship("PracticeTest", back_populates="roadmap")


class RoadmapProgress(Base):
    __tablename__ = "roadmap_progress"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    roadmap_id: Mapped[str] = mapped_column(String(36), ForeignKey("roadmaps.id", ondelete="CASCADE"), nullable=False)
    week_number: Mapped[int] = mapped_column(Integer, nullable=False)
    topic: Mapped[str] = mapped_column(String(200), nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    roadmap: Mapped["Roadmap"] = relationship("Roadmap", back_populates="progress_items")


class SkillGapAnalysis(Base):
    __tablename__ = "skill_gap_analyses"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    company: Mapped[str | None] = mapped_column(String(100), nullable=True)
    role: Mapped[str | None] = mapped_column(String(100), nullable=True)

    required_skills: Mapped[list] = mapped_column(JSON, default=list)
    user_skills: Mapped[list] = mapped_column(JSON, default=list)
    missing_skills: Mapped[list] = mapped_column(JSON, default=list)
    existing_skills: Mapped[list] = mapped_column(JSON, default=list)
    recommendations: Mapped[list] = mapped_column(JSON, default=list)
    match_score: Mapped[float] = mapped_column(Float, default=0.0)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
