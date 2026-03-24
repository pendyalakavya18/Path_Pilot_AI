"""
Production Flask Application for Render Deployment

This is a streamlined version of app.py optimized for production deployment:
- Uses fallback AI when Ollama is not available
- Supports in-memory data storage for ephemeral file systems
- Handles CORS for frontend-backend communication
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import os
import uuid
import json

# Try to import production config, fall back to default
try:
    from config_production import Config
except ImportError:
    from config import Config

# Try to import production data store, fall back to default
try:
    from data_store_production import DataStore
except ImportError:
    from data_store import DataStore

# Try to import fallback AI, fall back to original
try:
    from fallback_ai import fallback_ai
    HAS_FALLBACK_AI = True
except ImportError:
    HAS_FALLBACK_AI = False

# Import other modules
from knowledge_base import get_all_companies, get_company_roles

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY

# Enable CORS for frontend-backend communication
CORS(app, supports_credentials=True)

# Initialize data store based on environment
store_type = os.getenv('DATA_STORE_TYPE', 'file')
data_store = DataStore(store_type=store_type)

# Initialize AI engine (or use fallback)
USE_FALLBACK = os.getenv('USE_FALLBACK_AI', 'false').lower() == 'true'

# Import AI modules conditionally
ai_engine = None
rag_system = None

if not USE_FALLBACK:
    try:
        from ai_engine import OllamaEngine
        from rag_system import RAGSystem
        ai_engine = OllamaEngine()
        rag_system = RAGSystem()
        print("[AI] Using Ollama AI Engine")
    except Exception as e:
        print(f"[AI] Failed to initialize Ollama: {e}")
        print("[AI] Falling back to basic AI")
        USE_FALLBACK = True

if USE_FALLBACK or not ai_engine:
    print("[AI] Using Fallback AI (no Ollama required)")
    
    # Import roadmap generator with fallback
    try:
        from roadmap_generator import RoadmapGenerator
        roadmap_gen = RoadmapGenerator(fallback=True)
    except:
        # Create minimal roadmap generator with fallback
        class MinimalRoadmapGenerator:
            def __init__(self, fallback=True):
                self.fallback = fallback
                if fallback and HAS_FALLBACK_AI:
                    self.ai = fallback_ai
                else:
                    self.ai = None
            
            def create_roadmap(self, role, company, weeks, current_skills=None):
                if self.ai:
                    return self.ai.generate_roadmap(role, company, weeks, current_skills)
                return {'error': 'AI not available'}
            
            def get_weekly_details(self, roadmap, week_number):
                if roadmap and 'weekly_plan' in roadmap:
                    for week in roadmap['weekly_plan']:
                        if week.get('week') == week_number:
                            return week
                return None
        
        roadmap_gen = MinimalRoadmapGenerator(fallback=True)

# Initialize other modules
try:
    from skill_analyzer import SkillAnalyzer
    skill_analyzer = SkillAnalyzer()
except:
    class MinimalSkillAnalyzer:
        def analyze_gap(self, user_skills, company, role):
            return {'missing_skills': [], 'recommendations': []}
    skill_analyzer = MinimalSkillAnalyzer()

try:
    from test_generator import TestGenerator
    test_gen = TestGenerator()
except:
    class MinimalTestGenerator:
        def __init__(self):
            if HAS_FALLBACK_AI:
                self.ai = fallback_ai
            else:
                self.ai = None
        
        def generate_test(self, topic, num_questions=5):
            if self.ai:
                return self.ai.generate_practice_test(topic, num_questions)
            return []
        
        def evaluate_test(self, questions, answers):
            return {'score': 0, 'total': len(questions)}
    
    test_gen = MinimalTestGenerator()

try:
    from interview_engine import InterviewEngine
    interview_engine = InterviewEngine()
except:
    class MinimalInterviewEngine:
        def __init__(self):
            if HAS_FALLBACK_AI:
                self.ai = fallback_ai
            else:
                self.ai = None
        
        def start_interview(self, topic, difficulty, num_questions):
            if self.ai:
                return {'question': self.ai.generate_interview_question(topic, difficulty)}
            return {'question': 'Tell me about yourself'}
        
        def evaluate_response(self, question, response):
            if self.ai:
                return self.ai.evaluate_interview_response(question, response)
            return {'overall_score': 5, 'feedback': 'Good'}
        
        def get_interview_summary(self, evaluations):
            return {'average_score': 5, 'performance_level': 'Average'}
    
    interview_engine = MinimalInterviewEngine()

try:
    from progress_tracker import ProgressTracker
    progress_tracker = ProgressTracker()
except:
    class MinimalProgressTracker:
        def calculate_progress(self, roadmap, completed_weeks):
            return {'percentage': 0}
        def track_test_performance(self, test_results):
            return {'average': 0}
        def track_interview_performance(self, interviews):
            return {'average': 0}
        def calculate_overall_readiness(self, *args):
            return {'percentage': 0}
    
    progress_tracker = MinimalProgressTracker()


def get_user_id():
    """Get or create a user ID for the session"""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    return session['user_id']


# ==================== Routes ====================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    user_id = get_user_id()
    user = data_store.get_user(user_id)
    progress = data_store.get_progress(user_id)
    return render_template('dashboard.html', user=user, progress=progress)


@app.route('/profile')
def profile():
    user_id = get_user_id()
    user = data_store.get_user(user_id)
    return render_template('profile.html', user=user)


@app.route('/roadmap/create')
def roadmap_create():
    return render_template('roadmap_create.html')


@app.route('/roadmap/view')
def roadmap_view():
    import os
    user_id = get_user_id()
    roadmap = data_store.get_roadmap(user_id)
    
    # If no roadmap yet, load demo
    if not roadmap:
        demo_path = os.path.join(os.path.dirname(__file__), 'data', 'demo_roadmap.json')
        if os.path.exists(demo_path):
            with open(demo_path, 'r') as f:
                roadmap = json.load(f)
            data_store.save_roadmap(user_id, roadmap)
    
    return render_template('roadmap_view.html', roadmap=roadmap)


@app.route('/roadmap/week/<int:week_number>')
def weekly_plan(week_number):
    user_id = get_user_id()
    roadmap = data_store.get_roadmap(user_id)
    week_data = roadmap_gen.get_weekly_details(roadmap, week_number) if roadmap else None
    return render_template('weekly_plan.html', week=week_data, week_number=week_number)


@app.route('/practice-test')
def practice_test():
    return render_template('practice_test.html')


@app.route('/mock-interview')
def mock_interview():
    return render_template('mock_interview.html')


@app.route('/skill-gap')
def skill_gap():
    return render_template('skill_gap.html')


# ==================== API Routes ====================

@app.route('/api/profile', methods=['GET', 'POST'])
def api_profile():
    user_id = get_user_id()
    
    if request.method == 'POST':
        data = request.json
        user_data = {
            'name': data.get('name', ''),
            'skills': data.get('skills', []),
            'experience': data.get('experience', ''),
            'goals': data.get('goals', '')
        }
        data_store.save_user(user_id, user_data)
        return jsonify({'success': True, 'user': user_data})
    else:
        user = data_store.get_user(user_id)
        return jsonify({'user': user})


@app.route('/api/roadmap/generate', methods=['POST'])
def api_generate_roadmap():
    user_id = get_user_id()
    data = request.json
    
    role = data.get('role')
    company = data.get('company')
    weeks = int(data.get('weeks', 12))
    
    user = data_store.get_user(user_id)
    current_skills = user.get('skills', []) if user else None
    
    roadmap = roadmap_gen.create_roadmap(role, company, weeks, current_skills)
    data_store.save_roadmap(user_id, roadmap)
    
    return jsonify({'success': True, 'roadmap': roadmap})


@app.route('/api/roadmap', methods=['GET'])
def api_get_roadmap():
    user_id = get_user_id()
    roadmap = data_store.get_roadmap(user_id)
    return jsonify({'roadmap': roadmap})


@app.route('/api/skill-gap/analyze', methods=['POST'])
def api_analyze_skill_gap():
    user_id = get_user_id()
    data = request.json
    
    company = data.get('company')
    role = data.get('role')
    
    user = data_store.get_user(user_id)
    user_skills = user.get('skills', []) if user else []
    
    # Use fallback AI if available
    if HAS_FALLBACK_AI and USE_FALLBACK:
        from knowledge_base import get_company_skills
        required_skills = get_company_skills(company, role)
        analysis = fallback_ai.analyze_skill_gap(user_skills, required_skills)
    else:
        analysis = skill_analyzer.analyze_gap(user_skills, company, role)
    
    return jsonify({'success': True, 'analysis': analysis})


@app.route('/api/companies', methods=['GET'])
def api_get_companies():
    companies = get_all_companies()
    return jsonify({'companies': companies})


@app.route('/api/companies/<company>/roles', methods=['GET'])
def api_get_company_roles(company):
    roles = get_company_roles(company)
    return jsonify({'roles': roles})


@app.route('/api/test/generate', methods=['POST'])
def api_generate_test():
    data = request.json
    topic = data.get('topic')
    num_questions = int(data.get('num_questions', 5))
    
    test = test_gen.generate_test(topic, num_questions)
    
    return jsonify({'success': True, 'test': test})


@app.route('/api/test/submit', methods=['POST'])
def api_submit_test():
    user_id = get_user_id()
    data = request.json
    
    questions = data.get('questions', [])
    answers = data.get('answers', [])
    topic = data.get('topic', '')
    
    result = test_gen.evaluate_test(questions, answers)
    result['topic'] = topic
    
    data_store.save_test_result(user_id, result)
    
    return jsonify({'success': True, 'result': result})


@app.route('/api/interview/start', methods=['POST'])
def api_start_interview():
    data = request.json
    topic = data.get('topic')
    difficulty = data.get('difficulty', 'Medium')
    num_questions = int(data.get('num_questions', 5))
    
    interview = interview_engine.start_interview(topic, difficulty, num_questions)
    
    return jsonify({'success': True, 'interview': interview})


@app.route('/api/interview/evaluate', methods=['POST'])
def api_evaluate_response():
    data = request.json
    question = data.get('question')
    response = data.get('response')
    
    evaluation = interview_engine.evaluate_response(question, response)
    
    return jsonify({'success': True, 'evaluation': evaluation})


@app.route('/api/interview/submit', methods=['POST'])
def api_submit_interview():
    user_id = get_user_id()
    data = request.json
    
    interview_data = {
        'topic': data.get('topic'),
        'difficulty': data.get('difficulty'),
        'evaluations': data.get('evaluations', [])
    }
    
    summary = interview_engine.get_interview_summary(interview_data['evaluations'])
    interview_data['summary'] = summary
    
    data_store.save_interview(user_id, interview_data)
    
    return jsonify({'success': True, 'summary': summary})


@app.route('/api/progress', methods=['GET'])
def api_get_progress():
    user_id = get_user_id()
    
    roadmap = data_store.get_roadmap(user_id)
    test_results = data_store.get_test_results(user_id)
    interviews = data_store.get_interviews(user_id)
    
    progress_data = progress_tracker.calculate_progress(roadmap, [])
    test_performance = progress_tracker.track_test_performance(test_results)
    interview_performance = progress_tracker.track_interview_performance(interviews)
    readiness = progress_tracker.calculate_overall_readiness(progress_data, test_performance, interview_performance)
    
    return jsonify({
        'progress': progress_data,
        'test_performance': test_performance,
        'interview_performance': interview_performance,
        'readiness': readiness
    })


@app.route('/health')
def health_check():
    """Health check endpoint for Render"""
    return jsonify({
        'status': 'healthy',
        'ai_mode': 'fallback' if USE_FALLBACK else 'ollama',
        'store_type': store_type
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

