from flask import Flask, render_template, request, jsonify, session
from config import Config
from data_store import DataStore
from roadmap_generator import RoadmapGenerator
from skill_analyzer import SkillAnalyzer
from test_generator import TestGenerator
from interview_engine import InterviewEngine
from progress_tracker import ProgressTracker
from knowledge_base import get_all_companies, get_company_roles
import uuid
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY

data_store = DataStore()
roadmap_gen = RoadmapGenerator()
skill_analyzer = SkillAnalyzer()
test_gen = TestGenerator()
interview_engine = InterviewEngine()
progress_tracker = ProgressTracker()

def get_user_id():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    return session['user_id']

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
    
    # If no roadmap yet, silently load demo so the page always shows data
    if not roadmap:
        demo_path = os.path.join(os.path.dirname(__file__), 'data', 'demo_roadmap.json')
        if os.path.exists(demo_path):
            with open(demo_path, 'r') as f:
                roadmap = json.load(f)
            for week in roadmap.get('weekly_plan', []):
                week['resources'] = []
                for topic in week.get('topics', []):
                    resources = roadmap_gen.rag_system.get_resources_for_skill(topic, top_k=2)
                    week['resources'].extend(resources)
            data_store.save_roadmap(user_id, roadmap)
    
    return render_template('roadmap_view.html', roadmap=roadmap)

DEMO_ROADMAPS = {
    'google': 'demo_roadmap.json',
    'amazon': 'demo_roadmap_amazon.json',
    'meta':   'demo_roadmap_meta.json',
}

@app.route('/roadmap/load-demo')
def load_demo_roadmap_default():
    from flask import redirect, url_for
    return redirect(url_for('load_demo_roadmap', slug='google'))

@app.route('/roadmap/load-demo/<slug>')
def load_demo_roadmap(slug):
    """Load a pre-built demo roadmap for the current session."""
    import os
    from flask import redirect, url_for, abort
    if slug not in DEMO_ROADMAPS:
        abort(404)
    user_id = get_user_id()
    demo_path = os.path.join(os.path.dirname(__file__), 'data', DEMO_ROADMAPS[slug])
    with open(demo_path, 'r') as f:
        demo = json.load(f)
    for week in demo.get('weekly_plan', []):
        week['resources'] = []
        for topic in week.get('topics', []):
            resources = roadmap_gen.rag_system.get_resources_for_skill(topic, top_k=2)
            week['resources'].extend(resources)
    data_store.save_roadmap(user_id, demo)
    print(f"[DEMO] Loaded '{slug}' roadmap for user_id={user_id}")
    return redirect(url_for('roadmap_view'))

@app.route('/roadmap/week/<int:week_number>')
def weekly_plan(week_number):
    user_id = get_user_id()
    roadmap = data_store.get_roadmap(user_id)
    
    print(f"\n[WEEK VIEW] user_id={user_id}, week_number={week_number}")
    if roadmap:
        weekly_plan = roadmap.get('weekly_plan', [])
        print(f"[WEEK VIEW] roadmap has {len(weekly_plan)} weeks total")
    else:
        print(f"[WEEK VIEW] No roadmap found for this user_id in data store")
    
    week_data = roadmap_gen.get_weekly_details(roadmap, week_number) if roadmap else None
    print(f"[WEEK VIEW] week_data returned: {week_data}")
    
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
    
    print(f"\n{'='*60}")
    print(f"[ROADMAP] Generating: role='{role}', company='{company}', weeks={weeks}")
    print(f"[ROADMAP] User skills: {current_skills}")
    
    roadmap = roadmap_gen.create_roadmap(role, company, weeks, current_skills)
    
    # Log the result for debugging
    weekly_plan = roadmap.get('weekly_plan', [])
    print(f"[ROADMAP] Result: {len(weekly_plan)} weeks generated (requested {weeks})")
    if weekly_plan:
        print(f"[ROADMAP] First week sample: {weekly_plan[0]}")
    if 'error' in roadmap:
        print(f"[ROADMAP] ERROR: {roadmap['error']}")
    print(f"{'='*60}\n")
    
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
    
    # Build recent activity feed
    recent_activity = []
    for t in test_results[-5:]:
        recent_activity.append({
            'type': 'test',
            'title': f"Practice Test: {t.get('topic', 'Unknown')}",
            'score': f"{t.get('score', 0)}%",
            'timestamp': t.get('timestamp', ''),
            'level': t.get('performance_level', '')
        })
    for iv in interviews[-5:]:
        summary = iv.get('summary', {})
        recent_activity.append({
            'type': 'interview',
            'title': f"Mock Interview: {iv.get('topic', 'Unknown')}",
            'score': f"{summary.get('average_score', 0)}/10",
            'timestamp': iv.get('timestamp', ''),
            'level': summary.get('performance_level', '')
        })
    # Sort by timestamp descending, take last 5
    recent_activity.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    recent_activity = recent_activity[:5]
    
    return jsonify({
        'progress': progress_data,
        'test_performance': test_performance,
        'interview_performance': interview_performance,
        'readiness': readiness,
        'recent_activity': recent_activity
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
