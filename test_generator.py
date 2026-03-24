from ai_engine import OllamaEngine
from knowledge_base import get_interview_questions

class TestGenerator:
    def __init__(self):
        self.ai_engine = OllamaEngine()
    
    def generate_test(self, topic, num_questions=5):
        questions = self.ai_engine.generate_practice_test(topic, num_questions)
        
        return {
            'topic': topic,
            'num_questions': len(questions),
            'questions': questions
        }
    
    def evaluate_test(self, questions, user_answers):
        if len(questions) != len(user_answers):
            return {
                'error': 'Mismatch between questions and answers',
                'score': 0
            }
        
        correct_count = 0
        results = []
        
        for i, (question, user_answer) in enumerate(zip(questions, user_answers)):
            correct_answer = question.get('correct_answer', 0)
            is_correct = user_answer == correct_answer
            
            if is_correct:
                correct_count += 1
            
            results.append({
                'question_index': i,
                'question': question.get('question', ''),
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct,
                'explanation': question.get('explanation', '')
            })
        
        score = (correct_count / len(questions)) * 100 if questions else 0
        
        return {
            'total_questions': len(questions),
            'correct_answers': correct_count,
            'score': round(score, 2),
            'results': results,
            'performance_level': self._get_performance_level(score)
        }
    
    def _get_performance_level(self, score):
        if score >= 80:
            return 'Excellent'
        elif score >= 60:
            return 'Good'
        elif score >= 40:
            return 'Average'
        else:
            return 'Needs Improvement'
