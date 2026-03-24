import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class InterviewStartRequest(BaseModel):
    topic: str
    difficulty: str = "medium"   # easy | medium | hard
    num_questions: int = 5
    company: Optional[str] = None
    role: Optional[str] = None


class InterviewAnswerRequest(BaseModel):
    answer: str


class EvaluationResult(BaseModel):
    question: str
    answer: str
    technical_score: float
    communication_score: float
    problem_solving_score: float
    cultural_fit_score: float
    overall_score: float
    feedback: str
    follow_up_needed: bool = False
    follow_up_question: Optional[str] = None


class InterviewNextResponse(BaseModel):
    interview_id: uuid.UUID
    question: str
    question_index: int
    total_questions: int
    is_complete: bool
    evaluation: Optional[EvaluationResult] = None   # result of previous answer


class InterviewSummaryResponse(BaseModel):
    id: uuid.UUID
    topic: str
    difficulty: str
    overall_score: float
    technical_score: float
    communication_score: float
    confidence_score: float
    feedback: str
    strengths: list[str]
    improvements: list[str]
    evaluations: list[dict]
    created_at: datetime

    model_config = {"from_attributes": True}
