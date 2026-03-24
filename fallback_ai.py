"""
Fallback AI Engine for Production Deployment
Provides basic AI responses when Ollama is not available
"""

import json
import random

class FallbackAI:
    """Fallback AI that provides basic responses without requiring Ollama"""
    
    def __init__(self):
        self.fallback_mode = True
        
    def generate_roadmap(self, role, company, weeks, current_skills=None):
        """Generate a basic roadmap using templates"""
        current_skills = current_skills or []
        
        # Common tech skills for different roles
        common_skills = {
            'Software Engineer': ['Python', 'Java', 'Data Structures', 'Algorithms', 'System Design', 'Git'],
            'Data Scientist': ['Python', 'Machine Learning', 'Statistics', 'SQL', 'Data Analysis', 'Visualization'],
            'Frontend Engineer': ['JavaScript', 'React', 'HTML', 'CSS', 'TypeScript', 'Web Performance'],
            'Backend Engineer': ['Python', 'Java', 'Databases', 'API Design', 'Microservices', 'Docker'],
            'ML Engineer': ['Python', 'Machine Learning', 'TensorFlow', 'PyTorch', 'Deep Learning', 'NLP'],
            'DevOps Engineer': ['AWS', 'Docker', 'Kubernetes', 'CI/CD', 'Linux', 'Terraform'],
        }
        
        # Get skills for role or use default
        skills = common_skills.get(role, common_skills['Software Engineer'])
        
        # Generate weekly plan
        weekly_plan = []
        topics_pool = [
            'Fundamentals & Core Concepts',
            'Data Structures & Algorithms',
            'System Design Basics',
            'Advanced Topics',
            'Real-world Projects',
            'Testing & Best Practices',
            'Interview Preparation',
            'Portfolio Development'
        ]
        
        for week in range(1, weeks + 1):
            focus_topic = topics_pool[(week - 1) % len(topics_pool)]
            weekly_plan.append({
                'week': week,
                'focus': f"{focus_topic} - Week {week}",
                'topics': skills[:3],
                'hours_per_day': random.randint(2, 4),
                'milestones': [
                    f"Complete exercises on {skills[0]}",
                    f"Build a small project using {skills[1]}",
                    f"Review and practice {skills[2]}"
                ]
            })
        
        return {
            'role': role,
            'company': company,
            'duration_weeks': weeks,
            'weekly_plan': weekly_plan,
            'key_skills': skills,
            'recommended_projects': [
                f"Build a {role} portfolio project",
                f"Contribute to open source",
                f"Create a technical blog"
            ],
            'fallback_mode': True,
            'message': 'This is a basic roadmap. For personalized AI-generated content, please run the app locally with Ollama.'
        }
    
    def generate_practice_test(self, topic, num_questions=5):
        """Generate basic practice questions"""
        
        # Template questions for common topics
        question_templates = {
            'Python': [
                {'question': 'What is the time complexity of list.append()?', 'options': ['O(1)', 'O(n)', 'O(log n)', 'O(n²)'], 'correct_answer': 0, 'explanation': 'Appending to a list is O(1) amortized time complexity.'},
                {'question': 'Which data structure uses LIFO ordering?', 'options': ['Queue', 'Stack', 'Array', 'LinkedList'], 'correct_answer': 1, 'explanation': 'Stack uses Last In First Out (LIFO) ordering.'},
                {'question': 'What is a decorator in Python?', 'options': ['A design pattern', 'A function that modifies another function', 'A class attribute', 'A type of variable'], 'correct_answer': 1, 'explanation': 'A decorator is a function that takes another function as input and extends its behavior.'},
                {'question': 'What is the difference between == and is?', 'options': ['They are the same', '== compares value, is compares identity', 'is compares value, == compares identity', 'None of the above'], 'correct_answer': 1, 'explanation': '== compares values, is compares object identity (memory address).'},
                {'question': 'What is a lambda function?', 'options': ['A named function', 'An anonymous function', 'A recursive function', 'A generator'], 'correct_answer': 1, 'explanation': 'Lambda is an anonymous function defined with the lambda keyword.'},
            ],
            'JavaScript': [
                {'question': 'What does DOM stand for?', 'options': ['Document Object Model', 'Data Object Model', 'Digital Object Model', 'Dynamic Object Model'], 'correct_answer': 0, 'explanation': 'DOM stands for Document Object Model.'},
                {'question': 'Which keyword declares a constant?', 'options': ['var', 'let', 'const', 'constant'], 'correct_answer': 2, 'explanation': 'const declares a constant variable that cannot be reassigned.'},
                {'question': 'What is closure in JavaScript?', 'Options': ['A way to close files', 'A function with access to outer scope variables', 'An error handling mechanism', 'A type of loop'], 'correct_answer': 1, 'explanation': 'Closure is a function that has access to variables from its outer scope.'},
                {'question': 'What is the result of typeof null?', 'options': ['null', 'undefined', 'object', 'boolean'], 'correct_answer': 2, 'explanation': 'typeof null returns "object" - this is a known JavaScript quirk.'},
                {'question': 'Which method adds an element to the end of an array?', 'options': ['push()', 'pop()', 'shift()', 'unshift()'], 'correct_answer': 0, 'explanation': 'push() adds elements to the end of an array.'},
            ],
            'SQL': [
                {'question': 'Which SQL clause filters groups?', 'options': ['WHERE', 'HAVING', 'GROUP BY', 'ORDER BY'], 'correct_answer': 1, 'explanation': 'HAVING filters groups after GROUP BY aggregation.'},
                {'question': 'What does JOIN do?', 'options': ['Adds rows', 'Combines tables', 'Deletes data', 'Creates tables'], 'correct_answer': 1, 'explanation': 'JOIN combines rows from two or more tables based on a related column.'},
                {'question': 'Which is a primary key characteristic?', 'options': ['Can be null', 'Must be unique', 'Can be duplicated', 'Optional'], 'correct_answer': 1, 'explanation': 'Primary key must be unique and cannot be null.'},
                {'question': 'What does COUNT(*) return?', 'options': ['Sum of values', 'Number of rows', 'Average value', 'Maximum value'], 'correct_answer': 1, 'explanation': 'COUNT(*) counts all rows including nulls.'},
                {'question': 'Which normal form eliminates partial dependencies?', 'options': ['1NF', '2NF', '3NF', 'BCNF'], 'correct_answer': 1, 'explanation': '2NF eliminates partial dependencies on partial key.'},
            ],
        }
        
        # Get questions for topic or use default
        questions = question_templates.get(topic, question_templates['Python'])
        selected = random.sample(questions, min(num_questions, len(questions)))
        
        return selected
    
    def generate_interview_question(self, topic, difficulty):
        """Generate a basic interview question"""
        
        questions = {
            'Easy': [
                'Explain the difference between frontend and backend development.',
                'What version control systems have you used?',
                'Describe your experience with team projects.',
            ],
            'Medium': [
                'Explain the concept of RESTful APIs and their best practices.',
                'Describe a challenging bug you encountered and how you solved it.',
                'How would you design a scalable system for handling high traffic?',
            ],
            'Hard': [
                'Design a distributed system for real-time messaging like WhatsApp.',
                'Explain how you would implement a recommendation system for e-commerce.',
                'Describe the architecture you would use for a video streaming platform.',
            ]
        }
        
        difficulty_questions = questions.get(difficulty, questions['Medium'])
        selected = random.choice(difficulty_questions)
        
        return {
            'question': f"{topic}: {selected}",
            'hints': [
                'Think about the core concepts',
                'Consider real-world examples',
                'Break down the problem systematically'
            ],
            'key_points': [
                'Demonstrate understanding of fundamentals',
                'Show problem-solving approach',
                'Communicate clearly'
            ]
        }
    
    def evaluate_interview_response(self, question, response):
        """Provide basic evaluation"""
        
        # Simple keyword-based scoring
        score = 5
        feedback = "Good attempt! For more detailed feedback, please run the app locally with Ollama."
        
        if len(response) > 100:
            score = 7
            feedback = "You provided a detailed response. Consider adding more specific examples."
        
        if len(response) < 30:
            score = 3
            feedback = "Try to provide more detail in your answers."
        
        return {
            'technical_score': score,
            'communication_score': score + 1,
            'problem_solving_score': score,
            'cultural_fit_score': score,
            'overall_score': score,
            'feedback': feedback,
            'strengths': [
                'Attempted the question',
                'Showed willingness to participate'
            ],
            'improvements': [
                'Provide more specific examples',
                'Structure your answer better',
                'Practice more interview questions'
            ],
            'fallback_mode': True
        }
    
    def analyze_skill_gap(self, current_skills, required_skills):
        """Analyze skill gap"""
        
        current_set = set(current_skills or [])
        required_set = set(required_skills or [])
        
        missing = list(required_set - current_set)
        strong = list(current_set & required_set)
        
        return {
            'missing_skills': missing,
            'partial_skills': [],
            'strong_skills': strong,
            'priority_order': missing[:5],
            'recommendations': [
                f'Start learning {missing[0]} if available',
                'Practice coding problems regularly',
                'Build projects to apply your skills',
                'Prepare for system design interviews'
            ],
            'fallback_mode': True
        }


# Singleton instance
fallback_ai = FallbackAI()

