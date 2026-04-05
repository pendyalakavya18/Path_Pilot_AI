"""
llm_engine.py — ★ LLM CONNECTION POINT ★

Supports (all free / open-source options):
  - Groq API       (LLM_PROVIDER=groq)   <- recommended, FREE, fast open-source models
  - Ollama local   (LLM_PROVIDER=ollama) <- 100% local, no internet needed
  - OpenAI API     (LLM_PROVIDER=openai) <- paid

Groq is free at https://console.groq.com (no credit card).
Set LLM_PROVIDER=groq, GROQ_API_KEY=your_key in backend/.env
"""

import json
import re
from typing import Any
import httpx
from openai import AsyncOpenAI

from config import settings


class LLMEngine:
    def __init__(self):
        self._provider = settings.LLM_PROVIDER
        self._groq_clients = []
        self._current_groq_index = 0
        self._openai_client = None
        self._github_client = None

        if settings.LLM_PROVIDER == "groq":
            self._model = settings.GROQ_MODEL
            # Initialize a client for every Groq API key provided
            for key in settings.GROQ_API_KEYS:
                self._groq_clients.append(AsyncOpenAI(
                    api_key=key,
                    base_url="https://api.groq.com/openai/v1",
                ))
        elif settings.LLM_PROVIDER == "openai":
            self._model = settings.OPENAI_MODEL
            if settings.OPENAI_API_KEY:
                self._openai_client = AsyncOpenAI(
                    api_key=settings.OPENAI_API_KEY,
                    base_url=settings.OPENAI_BASE_URL,
                )
        else:
            self._model = settings.OLLAMA_MODEL

        # Initialize GitHub Copilot fallback if provided
        if settings.GITHUB_TOKEN:
            self._github_client = AsyncOpenAI(
                api_key=settings.GITHUB_TOKEN,
                base_url="https://models.inference.ai.azure.com",
            )

    # ── Internal helpers ─────────────────────────────────────────────

    async def _call(self, prompt: str, system: str = "You are a helpful AI career coach.") -> str:
        """Call LLM and return raw text response. Implements Universal Fallback (Groq -> Github -> OpenAI -> Ollama)."""
        
        # 1. Try Groq (Fastest/Free Cloud)
        if self._groq_clients:
            start_index = self._current_groq_index
            for i in range(len(self._groq_clients)):
                idx = (start_index + i) % len(self._groq_clients)
                client = self._groq_clients[idx]
                try:
                    response = await self._openai_compatible_call(client, settings.GROQ_MODEL, prompt, system)
                    self._current_groq_index = idx  # Remember the working key
                    return response
                except Exception as e:
                    print(f"[LLM WARNING] Groq key {idx+1}/{len(self._groq_clients)} failed: {e}")
        
        # 2. Try GitHub Copilot models
        if self._github_client:
            try:
                print(f"[LLM INFO] Trying GitHub Copilot fallback...")
                return await self._openai_compatible_call(self._github_client, "gpt-4o-mini", prompt, system)
            except Exception as e:
                print(f"[LLM WARNING] GitHub fallback failed: {e}")
                
        # 3. Try standard OpenAI
        if self._openai_client:
            try:
                print(f"[LLM INFO] Trying OpenAI fallback...")
                return await self._openai_compatible_call(self._openai_client, settings.OPENAI_MODEL, prompt, system)
            except Exception as e:
                print(f"[LLM WARNING] OpenAI fallback failed: {e}")

        # 4. Try Ollama (Local Fallback)
        try:
            print(f"[LLM INFO] Trying Local Ollama fallback...")
            return await self._ollama_call(prompt, system)
        except Exception as e:
            print(f"[LLM ERROR] All LLM providers failed. Last Ollama error: {e}")

        return ""

    async def _openai_compatible_call(self, client: AsyncOpenAI, model: str, prompt: str, system: str) -> str:
        """Works for Groq, OpenAI, and GitHub APIs."""
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=4096,
        )
        return response.choices[0].message.content or ""

    async def _ollama_call(self, prompt: str, system: str) -> str:
        full_prompt = f"{system}\n\n{prompt}"
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                f"{settings.OLLAMA_BASE_URL}/api/generate",
                json={"model": settings.OLLAMA_MODEL, "prompt": full_prompt, "stream": False},
            )
            response.raise_for_status()
            return response.json().get("response", "")

    def _parse_json(self, text: str, expected_type: type = dict) -> Any:
        """Extract JSON from LLM output (handles markdown code fences)."""
        # Try fenced code block first
        match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
        if match:
            text = match.group(1).strip()
        try:
            result = json.loads(text)
            if isinstance(result, expected_type):
                return result
        except json.JSONDecodeError:
            pass
        # Last resort: find first { or [ and parse from there
        for start_char, end_char, t in [("{", "}", dict), ("[", "]", list)]:
            start_idx = text.find(start_char)
            end_idx = text.rfind(end_char)
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx and isinstance(expected_type(), t):
                try:
                    res = json.loads(text[start_idx:end_idx+1])
                    if isinstance(res, expected_type):
                        return res
                except json.JSONDecodeError:
                    pass
        return expected_type()

    # ── Public AI methods ────────────────────────────────────────────

    async def generate_roadmap(
        self,
        role: str,
        company: str,
        weeks: int,
        current_skills: list[str],
        required_skills: list[str],
        missing_skills: list[str],
        context: list[dict],
    ) -> list[dict]:
        """
        Generate a week-by-week roadmap.
        Returns a list of week objects:
        [{ "week": 1, "theme": "...", "topics": [...], "hours_per_day": 2 }]
        """
        context_str = "\n".join(f"- {d.get('document','')}" for d in context[:8])
        required_str = ", ".join(required_skills[:12]) if required_skills else "General industry standards"
        missing_str = ", ".join(missing_skills[:10]) if missing_skills else "None identified"
        current_str = ", ".join(current_skills[:10]) if current_skills else "None"

        prompt = f"""
Create a {weeks}-week preparation roadmap for a student targeting:
  Company: {company}
  Role: {role}
  
Core requirements for this role at {company} (CRITICAL):
  {required_str}

Candidate Profile:
  Current skills: {current_str}
  Specific gaps (high priority): {missing_str}

Reference resources:
{context_str}

Rules:
- THE ROADMAP MUST PRIORITIZE THE CORE REQUIREMENTS listed above.
- Allocate MORE weeks to missing skills (high priority)
- Week 1 should build foundations, last week should focus on mock interviews
- Each week must be divided into exactly 5 days (e.g., day 1 to day 5)
- Each day must have EXACTLY ONE specific topic
- Topics must be concrete (e.g., "Binary Trees", "Dynamic Programming", not "Study harder")
- hours_per_day should be 2-4

Respond with ONLY a JSON array:
[
  {{
    "week": 1,
    "theme": "Foundational Concepts for {role} at {company}",
    "days": [
      {{"day": 1, "topic": "Specific topic relevant to {required_str}"}},
      ...
    ],
    "hours_per_day": 2,
    "focus": "Building core foundations specifically for {company}'s tech stack"
  }},
  ...
]
"""
        raw = await self._call(prompt)
        plan = self._parse_json(raw, list)
        if not isinstance(plan, list) or not plan:
            return self._fallback_roadmap(weeks, role, company, required_skills)
        return plan

    async def generate_practice_test(
        self,
        topic: str,
        num_questions: int,
        context: list[dict],
    ) -> list[dict]:
        """
        Generate MCQ questions for `topic`.
        Returns list: [{ question, options[4], correct_answer(int 0-3), explanation }]
        """
        context_str = "\n".join(f"- {d.get('document','')}" for d in context[:5])

        prompt = f"""
Generate {num_questions} multiple-choice questions about: {topic}

Reference material:
{context_str}

Rules:
- Questions must be specific to "{topic}" — not generic
- Include conceptual, application, and tricky edge-case questions
- Each question has exactly 4 options
- correct_answer is the 0-based index of the right option
- Include a brief explanation

Respond with ONLY a JSON array:
[
  {{
    "question": "What is the time complexity of binary search?",
    "options": ["O(n)", "O(log n)", "O(n²)", "O(1)"],
    "correct_answer": 1,
    "explanation": "Binary search halves the search space each step, giving O(log n)."
  }},
  ...
]
"""
        raw = await self._call(prompt)
        questions = self._parse_json(raw, list)
        if not isinstance(questions, list) or not questions:
            return self._fallback_test(topic, num_questions)
        return questions[:num_questions]

    async def generate_interview_question(
        self, topic: str, difficulty: str, context: list[dict]
    ) -> dict:
        """Generate a single interview question with hints."""
        context_str = "\n".join(f"- {d.get('document','')}" for d in context[:3])
        prompt = f"""
Generate one {difficulty}-level interview question for: {topic}

Context:
{context_str}

Respond with ONLY JSON:
{{
  "question": "...",
  "type": "technical",
  "hints": ["hint 1", "hint 2"],
  "key_points": ["point 1", "point 2"],
  "expected_duration_minutes": 5
}}
"""
        raw = await self._call(prompt)
        result = self._parse_json(raw, dict)
        if not result.get("question"):
            return self._fallback_interview_question(topic, difficulty)
        return result

    async def evaluate_interview_response(self, question: str, answer: str) -> dict:
        """
        Evaluate a candidate's answer on 4 dimensions (0-10 each).
        Returns: {technical, communication, problem_solving, cultural_fit, overall, feedback, follow_up_needed}
        """
        prompt = f"""
You are a senior technical interviewer at a top tech company.
Evaluate this interview response:

Question: {question}
Candidate's Answer: {answer}

Score each dimension 0-10:
- technical: accuracy, depth, correctness
- communication: clarity, structure, articulation
- problem_solving: approach, creativity, edge cases
- cultural_fit: enthusiasm, collaboration mindset

Also decide if a follow-up question is needed (true if overall score < 6).

Respond with ONLY JSON:
{{
  "technical": 7,
  "communication": 6,
  "problem_solving": 7,
  "cultural_fit": 8,
  "overall": 7.0,
  "feedback": "Good answer covering the main points. Could improve by discussing edge cases.",
  "follow_up_needed": false,
  "follow_up_question": null
}}
"""
        raw = await self._call(prompt)
        result = self._parse_json(raw, dict)
        if not result:
            result = {"technical": 5, "communication": 5, "problem_solving": 5, "cultural_fit": 5,
                      "feedback": "Answer noted. Keep practicing!", "follow_up_needed": False}
        # Calculate weighted overall if not set
        if "overall" not in result or not result["overall"]:
            weights = settings.SCORING_WEIGHTS
            result["overall"] = round(
                result.get("technical", 5) * weights["technical"]
                + result.get("communication", 5) * weights["communication"]
                + result.get("problem_solving", 5) * weights["problem_solving"]
                + result.get("cultural_fit", 5) * weights["cultural_fit"],
                2,
            )
        return result

    async def analyze_resume(
        self, resume_text: str, target_company: str, target_role: str
    ) -> dict:
        """Extract structured info from resume text and perform gap analysis."""
        prompt = f"""
Analyze this resume text and extract structured information.
Target: {target_company} — {target_role}

Resume:
{resume_text[:4000]}

Respond with ONLY JSON:
{{
  "name": "...",
  "email": "...",
  "skills": ["Python", "SQL", "React"],
  "experience_years": 1.5,
  "education": {{"degree": "B.Tech", "branch": "CSE", "cgpa": 8.5, "year": 2025}},
  "projects": ["project 1", "project 2"],
  "skill_gap": {{
    "missing": ["DSA", "System Design"],
    "existing": ["Python", "SQL"],
    "priority_order": ["DSA", "System Design"]
  }},
  "recommendations": [
    "Practice 2 LeetCode problems daily",
    "Study System Design from Grokking the System Design Interview"
  ]
}}
"""
        raw = await self._call(prompt)
        result = self._parse_json(raw, dict)
        if not result:
            result = {
                "skills": [], "experience_years": 0,
                "education": {}, "projects": [],
                "skill_gap": {"missing": [], "existing": [], "priority_order": []},
                "recommendations": ["Upload a clearer resume for better analysis."],
            }
        return result

    async def generate_roadmap_summary(self, evals: list[dict]) -> dict:
        """Generate overall interview summary from all evaluations."""
        scores = [e.get("overall", 5) for e in evals]
        avg = sum(scores) / len(scores) if scores else 0

        prompt = f"""
Summarize this mock interview session:
- Questions answered: {len(evals)}
- Average score: {avg:.1f}/10
- Per-question evaluations: {json.dumps(evals[:5], indent=2)}

Generate a professional summary. Respond with ONLY JSON:
{{
  "overall_score": {avg:.1f},
  "technical_score": 7.0,
  "communication_score": 6.5,
  "confidence_score": 7.0,
  "feedback": "Overall strong performance...",
  "strengths": ["Clear explanations", "Good problem-solving"],
  "improvements": ["Practice more edge cases", "Be more concise"]
}}
"""
        raw = await self._call(prompt)
        result = self._parse_json(raw, dict)
        result.setdefault("overall_score", round(avg, 2))
        return result

    # ── Fallbacks ────────────────────────────────────────────────────

    def _fallback_roadmap(self, weeks: int, role: str, company: str, required_skills: list[str]) -> list[dict]:
        themes = [
            f"Foundations & Core Context for {role}",
            f"Key Tools & Methodologies at {company}",
            "Intermediate Application",
            "Advanced Scenarios",
            "System / Process Design",
            "Interview Prep & Best Practices",
        ]
        plan = []
        for i in range(weeks):
            theme = themes[i % len(themes)]
            days = []
            for d in range(5):
                skill = required_skills[d % len(required_skills)] if required_skills else f"Essential Concept {d + 1}"
                days.append({"day": d + 1, "topic": f"Mastering {skill} for {company}"})
            
            plan.append({
                "week": i + 1,
                "theme": theme,
                "days": days,
                "hours_per_day": 2,
                "focus": f"Mastering {theme} skills specifically tailored to {company}"
            })
        return plan

    def _fallback_test(self, topic: str, num_questions: int) -> list[dict]:
        """Template MCQ questions when LLM is unavailable."""
        templates = [
            {
                "question": f"Which of the following best describes '{topic}'?",
                "options": [
                    f"A core concept in {topic}",
                    f"An unrelated programming concept",
                    f"A database operation",
                    f"A network protocol",
                ],
                "correct_answer": 0,
                "explanation": f"Option A correctly describes the core nature of {topic}.",
            },
            {
                "question": f"What is the primary purpose of studying {topic}?",
                "options": [
                    "To pass interviews at top tech companies",
                    "To build scalable software systems",
                    "To understand computer science fundamentals",
                    "All of the above",
                ],
                "correct_answer": 3,
                "explanation": "Studying this topic helps with all of the listed goals.",
            },
            {
                "question": f"Which skill is most closely related to {topic}?",
                "options": ["Problem solving", "Data modeling", "UI design", "Network configuration"],
                "correct_answer": 0,
                "explanation": "Problem solving is fundamental to mastering this topic.",
            },
        ]
        return [templates[i % len(templates)] for i in range(num_questions)]

    def _fallback_interview_question(self, topic: str, difficulty: str) -> dict:
        """Template interview question when LLM is unavailable."""
        questions = {
            "easy": f"Can you explain the basic concept of {topic} in simple terms?",
            "medium": f"How would you implement a solution using {topic}? Walk me through your approach.",
            "hard": f"Design a system that leverages {topic} at scale. What trade-offs would you consider?",
        }
        return {
            "question": questions.get(difficulty, questions["medium"]),
            "type": "technical",
            "hints": [f"Think about the core principles of {topic}", "Consider time and space complexity"],
            "key_points": [f"Understanding of {topic}", "Clear communication", "Edge case handling"],
            "expected_duration_minutes": 5,
        }


# Module-level singleton
llm_engine = LLMEngine()
