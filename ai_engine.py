import requests
import json
import re
from config import Config


# Common placeholder values that TinyLlama may copy from prompt templates
PLACEHOLDER_PATTERNS = [
    'skill1', 'skill2', 'skill3', 'skill4',
    'subtopic1', 'subtopic2',
    'topic name', 'topic_name',
    'project1', 'project2',
    'milestone1', 'milestone2',
    'hint1', 'hint2',
    'point1', 'point2',
    'strength1', 'strength2',
    'improvement1', 'improvement2',
    'recommendation1', 'recommendation2',
    'skill to learn first', 'skill to learn second',
    'detailed feedback',
    'question text here',
    'option a', 'option b', 'option c', 'option d',
    'why this is the correct answer',
]


def _contains_placeholders(data, depth=0):
    if depth > 5:
        return False
    if isinstance(data, str):
        lower = data.strip().lower()
        return any(lower == p for p in PLACEHOLDER_PATTERNS)
    elif isinstance(data, list):
        placeholder_count = sum(1 for item in data if _contains_placeholders(item, depth + 1))
        return placeholder_count > len(data) * 0.4 if data else False
    elif isinstance(data, dict):
        for v in data.values():
            if _contains_placeholders(v, depth + 1):
                return True
    return False


class OllamaEngine:
    def __init__(self):
        self.base_url = Config.OLLAMA_BASE_URL
        self.model = Config.OLLAMA_MODEL
        self.generate_url = f"{self.base_url}/api/generate"

    def _generate(self, prompt):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        try:
            resp = requests.post(self.generate_url, json=payload, timeout=600)
            resp.raise_for_status()
            return resp.json().get("response", "")
        except requests.RequestException as e:
            print(f"[OllamaEngine] Request failed: {e}")
            return ""

    def _extract_json(self, text):
        if not text:
            return None
        fence_match = re.search(r'```(?:json)?\s*([\s\S]*?)```', text)
        if fence_match:
            candidate = fence_match.group(1).strip()
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                pass
        for pattern in [r'(\{[\s\S]*\})', r'(\[[\s\S]*\])']:
            match = re.search(pattern, text)
            if match:
                try:
                    return json.loads(match.group(1))
                except json.JSONDecodeError:
                    continue
        try:
            return json.loads(text.strip())
        except json.JSONDecodeError:
            return None

    def _generate_json(self, prompt, expect_type=dict, max_retries=2):
        for attempt in range(max_retries + 1):
            text = self._generate(prompt)
            parsed = self._extract_json(text)
            if parsed is None:
                continue
            if not isinstance(parsed, expect_type):
                continue
            if _contains_placeholders(parsed):
                print(f"[OllamaEngine] Placeholder detected (attempt {attempt + 1}), retrying...")
                continue
            return parsed
        return None

    # -- Roadmap -----------------------------------------------------------

    def generate_roadmap(self, role, company, weeks, current_skills=None):
        current_skills_str = ', '.join(current_skills) if current_skills else 'beginner level'

        prompt = (
            "You are a career mentor. Create a " + str(weeks) + "-week learning roadmap "
            "for a " + str(role) + " at " + str(company) + ".\n"
            "The learner already knows: " + current_skills_str + ".\n\n"
            "Reply with ONLY a JSON object. You MUST generate exactly " + str(weeks) + " weeks "
            "in the weekly_plan array. Here is the structure with only week 1 as example, "
            "but you must include week 1 through week " + str(weeks) + ":\n\n"
            '{\n'
            '  "role": "' + str(role) + '",\n'
            '  "company": "' + str(company) + '",\n'
            '  "duration_weeks": ' + str(weeks) + ',\n'
            '  "weekly_plan": [\n'
            '    {\n'
            '      "week": 1,\n'
            '      "focus": "Python fundamentals and data types",\n'
            '      "topics": ["Variables and data types", "Control flow and loops", "Functions and modules"],\n'
            '      "hours_per_day": 2,\n'
            '      "milestones": ["Complete 10 coding exercises", "Build a calculator program"]\n'
            '    }\n'
            '  ],\n'
            '  "key_skills": ["Python", "SQL", "Data Analysis", "Statistics"],\n'
            '  "recommended_projects": ["Build a data pipeline for CSV processing", "Create a dashboard with Streamlit"]\n'
            '}\n\n'
            "CRITICAL RULES:\n"
            "- Generate ALL " + str(weeks) + " weeks (week 1 through week " + str(weeks) + "), each with unique focus areas\n"
            "- Every field must have real, specific content relevant to " + str(role) + " at " + str(company) + "\n"
            "- Do NOT write skill1 or topic name, use actual names\n"
            "- Do NOT stop at 1 or 2 weeks, the weekly_plan array MUST have " + str(weeks) + " entries\n"
            "- Return ONLY valid JSON, no other text"
        )

        parsed = self._generate_json(prompt, dict)
        if parsed:
            if parsed.get('weekly_plan') and len(parsed['weekly_plan']) > 0:
                return parsed

        return {
            'role': role,
            'company': company,
            'duration_weeks': weeks,
            'weekly_plan': [],
            'error': 'Failed to generate roadmap. Please try again.'
        }

    # -- Practice Test -----------------------------------------------------

    def generate_practice_test(self, topic, num_questions=5):
        prompt = (
            "You are a technical interviewer. Generate " + str(num_questions) + " multiple-choice "
            "questions about " + str(topic) + ".\n\n"
            "Reply with ONLY a JSON array. Each question must be specific and technical:\n\n"
            '[\n'
            '  {\n'
            '    "question": "What is the time complexity of binary search on a sorted array of n elements?",\n'
            '    "options": ["O(n)", "O(log n)", "O(n log n)", "O(1)"],\n'
            '    "correct_answer": 1,\n'
            '    "explanation": "Binary search halves the search space in each step, giving O(log n) complexity."\n'
            '  }\n'
            ']\n\n'
            "Generate exactly " + str(num_questions) + " questions about " + str(topic) + ". "
            "Every question must be specific, technical, and have exactly 4 options. "
            "Do NOT use placeholder text."
        )

        parsed = self._generate_json(prompt, list)
        if parsed and len(parsed) > 0:
            valid = [q for q in parsed if isinstance(q, dict) and q.get('question') and not _contains_placeholders(q)]
            return valid if valid else []
        return []

    # -- Interview Question ------------------------------------------------

    def generate_interview_question(self, topic, difficulty):
        prompt = (
            "You are a technical interviewer asking a " + str(difficulty) + "-level question "
            "about " + str(topic) + ".\n\n"
            "Generate exactly ONE technical interview question. Reply with ONLY a JSON object:\n\n"
            '{\n'
            '  "question": "Explain how a hash table handles collisions and compare chaining vs open addressing.",\n'
            '  "hints": ["Think about what happens when two keys map to the same bucket", "Consider the trade-offs in memory usage"],\n'
            '  "key_points": ["Hash function distributes keys to buckets", "Chaining uses linked lists at each bucket", "Open addressing probes for the next empty slot"]\n'
            '}\n\n'
            "The question MUST be a specific, technical question about " + str(topic) + " at "
            + str(difficulty) + " level. Do NOT ask vague questions like tell me about or "
            "summarize the main points. Ask something that tests real knowledge."
        )

        parsed = self._generate_json(prompt, dict)
        if parsed and parsed.get('question'):
            return parsed
        return {
            'question': 'Explain the core concepts of ' + str(topic) + ' and how they are applied in real-world software systems.',
            'hints': ['Think about the fundamental principles of ' + str(topic)],
            'key_points': ['Cover the key aspects of ' + str(topic)]
        }

    # -- Interview Evaluation ----------------------------------------------

    def evaluate_interview_response(self, question, response):
        prompt = (
            "You are evaluating a job interview answer.\n\n"
            "Question: " + str(question) + "\n"
            "Candidate answer: " + str(response) + "\n\n"
            "Rate the answer on a scale of 1 to 10 for each category. Be fair but honest. "
            "Reply with ONLY a JSON object:\n\n"
            '{\n'
            '  "technical_score": 7,\n'
            '  "communication_score": 8,\n'
            '  "problem_solving_score": 6,\n'
            '  "cultural_fit_score": 7,\n'
            '  "overall_score": 7,\n'
            '  "feedback": "Good understanding of the concept with clear explanation. Could improve by providing more concrete examples.",\n'
            '  "strengths": ["Clear explanation of core concepts", "Good use of real-world examples"],\n'
            '  "improvements": ["Add more detail about edge cases", "Discuss performance trade-offs"]\n'
            '}\n\n'
            "Score each category from 1 to 10 based on the actual quality of the answer. "
            "Write specific feedback about THIS answer. Do NOT use placeholder text."
        )

        parsed = self._generate_json(prompt, dict)
        if parsed and parsed.get('feedback') and parsed['feedback'] != 'Detailed feedback':
            for key in ['technical_score', 'communication_score', 'problem_solving_score', 'cultural_fit_score', 'overall_score']:
                val = parsed.get(key)
                if not isinstance(val, (int, float)) or val < 1 or val > 10:
                    parsed[key] = 5
            return parsed

        return {
            'technical_score': 5,
            'communication_score': 5,
            'problem_solving_score': 5,
            'cultural_fit_score': 5,
            'overall_score': 5,
            'feedback': 'Unable to evaluate response',
            'strengths': [],
            'improvements': []
        }

    # -- Skill Gap Analysis ------------------------------------------------

    def analyze_skill_gap(self, current_skills, required_skills):
        current_str = ', '.join(current_skills) if current_skills else 'none'
        required_str = ', '.join(required_skills) if required_skills else 'none'

        prompt = (
            "Analyze the gap between a candidate current skills and the skills required for the job.\n\n"
            "Current skills: " + current_str + "\n"
            "Required skills: " + required_str + "\n\n"
            "Reply with ONLY a JSON object. Fill in real skills from the lists above:\n\n"
            '{\n'
            '  "missing_skills": ["SQL", "System Design"],\n'
            '  "partial_skills": ["Python"],\n'
            '  "strong_skills": ["JavaScript", "React"],\n'
            '  "priority_order": ["SQL", "System Design"],\n'
            '  "recommendations": ["Start with SQL basics using SQLZoo", "Study system design patterns from the System Design Primer"]\n'
            '}\n\n'
            "Use the ACTUAL skill names from the lists above. Do NOT use placeholders like skill1."
        )

        parsed = self._generate_json(prompt, dict)
        if parsed and not _contains_placeholders(parsed):
            return parsed

        return {
            'missing_skills': list(set(required_skills) - set(current_skills)),
            'partial_skills': [],
            'strong_skills': current_skills,
            'priority_order': list(set(required_skills) - set(current_skills)),
            'recommendations': ['Focus on learning ' + s for s in list(set(required_skills) - set(current_skills))[:3]]
        }
