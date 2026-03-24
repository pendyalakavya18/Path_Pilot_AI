from ai_engine import OllamaEngine
from config import Config
from knowledge_base import INTERVIEW_QUESTION_TEMPLATES
from datetime import datetime
import random

# Phrases that indicate a vague, non-technical question
BAD_QUESTION_PHRASES = [
    'provide a clear and concise summary',
    'summarize the main points',
    'can you summarize',
    'describe your general experience',
    'tell me about yourself',
    'what are your strengths',
    'what are your weaknesses',
    'why do you want to work',
    'where do you see yourself',
    'walk me through your resume',
    'main points covered',
    'provide a summary',
    'give a brief overview of your',
    'what motivates you',
]


def _is_valid_question(question_data, topic):
    """Check if a question is specific and technical enough."""
    if not isinstance(question_data, dict):
        return False
    q_text = question_data.get('question', '').strip()
    if not q_text or len(q_text) < 15:
        return False
    q_lower = q_text.lower()
    for phrase in BAD_QUESTION_PHRASES:
        if phrase in q_lower:
            return False
    if q_lower == ('tell me about ' + str(topic)).lower():
        return False
    return True


def _get_template_question(topic, difficulty, used_indices=None):
    """Get a curated question from the knowledge base as fallback."""
    if used_indices is None:
        used_indices = set()

    # Try to get questions for this exact difficulty
    templates = INTERVIEW_QUESTION_TEMPLATES.get(difficulty, {})

    # Try exact topic match first
    questions = templates.get(topic, [])
    if not questions:
        # Try partial match within this difficulty
        for key in templates:
            if key.lower() in topic.lower() or topic.lower() in key.lower():
                questions = templates[key]
                break

    if not questions:
        # Fallback: any topic within this difficulty
        for qs in templates.values():
            questions.extend(qs)

    if not questions:
        # Last resort: any difficulty, any topic
        for diff_templates in INTERVIEW_QUESTION_TEMPLATES.values():
            for qs in diff_templates.values():
                questions.extend(qs)

    available = [(i, q) for i, q in enumerate(questions) if i not in used_indices]
    if not available:
        available = list(enumerate(questions))

    if not available:
        return {
            'question': f'Explain how {topic} works and its key use cases.',
            'hints': [f'Focus on core concepts of {topic}'],
            'key_points': [f'Cover practical applications of {topic}']
        }

    idx, q_text = random.choice(available)
    used_indices.add(idx)
    return {
        'question': q_text,
        'hints': [f'Think about the core concepts of this topic'],
        'key_points': [f'Focus on practical knowledge and real-world applications']
    }


class InterviewEngine:
    def __init__(self):
        self.ai_engine = OllamaEngine()

    def start_interview(self, topic, difficulty, num_questions=5):
        # Normalize difficulty
        difficulty = difficulty.capitalize()
        if difficulty not in ('Easy', 'Medium', 'Hard'):
            difficulty = 'Medium'

        questions = []
        used_template_indices = set()

        for _ in range(num_questions):
            question = self.ai_engine.generate_interview_question(topic, difficulty)

            if _is_valid_question(question, topic):
                questions.append(question)
            else:
                fallback = _get_template_question(topic, difficulty, used_template_indices)
                questions.append(fallback)

        return {
            'topic': topic,
            'difficulty': difficulty,
            'questions': questions,
            'current_question': 0,
            'started_at': datetime.now().isoformat()
        }

    def evaluate_response(self, question, response):
        evaluation = self.ai_engine.evaluate_interview_response(question, response)

        overall_score = self._calculate_overall_score(
            evaluation.get('technical_score', 5),
            evaluation.get('communication_score', 5),
            evaluation.get('problem_solving_score', 5),
            evaluation.get('cultural_fit_score', 5)
        )

        evaluation['overall_score'] = overall_score
        return evaluation

    def _calculate_overall_score(self, technical, communication, problem_solving, cultural_fit):
        weights = Config.SCORING_WEIGHTS
        score = (
            technical * weights['technical'] +
            communication * weights['communication'] +
            problem_solving * weights['problem_solving'] +
            cultural_fit * weights['cultural_fit']
        )
        return round(score, 2)

    def get_interview_summary(self, evaluations):
        if not evaluations:
            return {
                'average_score': 0,
                'total_questions': 0,
                'strengths': [],
                'improvements': []
            }

        total_score = sum(e.get('overall_score', 0) for e in evaluations)
        avg_score = total_score / len(evaluations)

        all_strengths = []
        all_improvements = []
        for evaluation in evaluations:
            all_strengths.extend(evaluation.get('strengths', []))
            all_improvements.extend(evaluation.get('improvements', []))

        return {
            'average_score': round(avg_score, 2),
            'total_questions': len(evaluations),
            'performance_level': self._get_performance_level(avg_score),
            'strengths': list(set(all_strengths)),
            'improvements': list(set(all_improvements)),
            'score_breakdown': {
                'technical': round(sum(e.get('technical_score', 0) for e in evaluations) / len(evaluations), 2),
                'communication': round(sum(e.get('communication_score', 0) for e in evaluations) / len(evaluations), 2),
                'problem_solving': round(sum(e.get('problem_solving_score', 0) for e in evaluations) / len(evaluations), 2),
                'cultural_fit': round(sum(e.get('cultural_fit_score', 0) for e in evaluations) / len(evaluations), 2)
            }
        }

    def _get_performance_level(self, score):
        if score >= 8:
            return 'Excellent'
        elif score >= 6:
            return 'Good'
        elif score >= 4:
            return 'Average'
        else:
            return 'Needs Improvement'
