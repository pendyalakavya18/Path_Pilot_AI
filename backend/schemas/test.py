import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TestGenerateRequest(BaseModel):
    topic: str
    num_questions: int = 10
    roadmap_id: Optional[uuid.UUID] = None


class TestSubmitRequest(BaseModel):
    test_id: uuid.UUID
    answers: list[int]  # list of chosen option indices


class QuestionResult(BaseModel):
    question: str
    options: list[str]
    correct_answer: int
    user_answer: int
    is_correct: bool
    explanation: Optional[str] = None


class TestResultResponse(BaseModel):
    id: uuid.UUID
    topic: str
    score: float
    total_questions: int
    performance_level: str
    results: list[QuestionResult]
    taken_at: datetime

    model_config = {"from_attributes": True}
