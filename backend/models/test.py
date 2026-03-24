import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class PracticeTest(Base):
    __tablename__ = "practice_tests"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    roadmap_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("roadmaps.id", ondelete="SET NULL"), nullable=True)

    topic: Mapped[str] = mapped_column(String(200), nullable=False)

    # AI-generated MCQ + coding questions
    questions: Mapped[list] = mapped_column(JSON, default=list)
    # User's submitted answers (list of answer indices)
    user_answers: Mapped[list] = mapped_column(JSON, default=list)

    score: Mapped[float | None] = mapped_column(Float, nullable=True)
    total_questions: Mapped[int] = mapped_column(Integer, default=0)
    performance_level: Mapped[str | None] = mapped_column(String(50), nullable=True)

    taken_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="tests")
    roadmap: Mapped["Roadmap"] = relationship("Roadmap", back_populates="tests")
