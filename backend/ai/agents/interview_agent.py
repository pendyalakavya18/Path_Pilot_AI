"""
interview_agent.py — AI Interview Agent

Manages the full conversation state for a mock interview:
  1. Generates a bank of questions (RAG + LLM)
  2. Evaluates each answer in real-time
  3. Decides whether a follow-up is needed
  4. Produces a final interview summary
"""

from ai.llm_engine import llm_engine
from ai.rag_pipeline import rag_pipeline
from ai.knowledge_base import get_interview_questions


class InterviewAgent:

    async def generate_questions(
        self, topic: str, difficulty: str, num_questions: int
    ) -> list[dict]:
        """Generate a bank of questions using RAG + LLM."""
        # Retrieve similar questions from vector DB for context
        context = await rag_pipeline.search(
            query=f"{difficulty} interview questions about {topic}",
            collection="interview_questions",
            top_k=10,
        )

        questions = []
        for i in range(num_questions):
            q = await llm_engine.generate_interview_question(
                topic=topic,
                difficulty=difficulty,
                context=context[i % len(context) : i % len(context) + 3] if context else [],
            )
            if not q or not q.get("question"):
                # Fall back to template bank
                templates = get_interview_questions(topic, difficulty)
                if templates:
                    q = {"question": templates[i % len(templates)], "type": "technical", "hints": [], "key_points": []}
                else:
                    continue
            questions.append(q)

        return questions

    async def generate_next_question(
        self, topic: str, difficulty: str, history: list[dict], target_skills: list[str] = None
    ) -> dict:
        """Dynamically generate the next question based on history and target company skills."""
        history_str = ""
        for i, h in enumerate(history[-3:]): # Use last 3 for concise context
            history_str += f"Q: {h.get('question')}\nA: {h.get('answer')}\nScore: {h.get('overall', 5)}/10\n\n"

        target_context = ""
        if target_skills:
            target_context = f"\nFocus on these company-specific required skills if relevant: {', '.join(target_skills[:5])}"

        prompt = f"""
You are conducting a {difficulty}-level interview on {topic}.
{target_context}

Recent context:
{history_str}

Based on the candidate's previous answers and the target skills, generate the NEXT question.
If they struggled, ask a related foundational question.
If they did well, dive deeper or introduce a new sub-topic.

Respond with ONLY JSON:
{{
  "question": "...",
  "type": "technical",
  "hints": ["hint 1", "hint 2"],
  "key_points": ["point 1", "point 2"],
  "expected_duration_minutes": 5
}}
"""
        raw = await llm_engine._call(prompt)
        import json
        result = llm_engine._parse_json(raw, dict)
        if not result or not result.get("question"):
            return {"question": f"Follow-up: regarding {topic}, can you elaborate on a related advanced concept?", "type": "technical", "hints": [], "key_points": []}
        return result

    async def evaluate_answer(self, question: str, answer: str) -> dict:
        """Evaluate a single answer. Returns scores + feedback + follow_up decision."""
        return await llm_engine.evaluate_interview_response(question=question, answer=answer)

    async def generate_follow_up(self, original_question: str, weak_answer: str) -> str:
        """Generate a follow-up question when the answer was insufficient."""
        context = await rag_pipeline.search(
            query=original_question,
            collection="interview_questions",
            top_k=3,
        )
        prompt = f"""
The candidate gave an insufficient answer to this question:
Question: {original_question}
Weak Answer: {weak_answer}

Generate ONE targeted follow-up question to dig deeper.
Respond with ONLY the question text (no JSON, no extra text).
"""
        # Use LLM directly for a simple string response
        raw = await llm_engine._call(prompt)
        return raw.strip().strip('"').strip("'")

    async def generate_summary(self, evaluations: list[dict]) -> dict:
        """Aggregate all evaluations into a final interview summary."""
        return await llm_engine.generate_roadmap_summary(evaluations)
