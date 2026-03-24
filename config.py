import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'tinyllama')
    EMBEDDING_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'
    
    MAX_ROADMAP_WEEKS = 24
    MIN_ROADMAP_WEEKS = 4
    
    INTERVIEW_DIFFICULTIES = ['Easy', 'Medium', 'Hard']
    
    SCORING_WEIGHTS = {
        'technical': 0.4,
        'communication': 0.3,
        'problem_solving': 0.2,
        'cultural_fit': 0.1
    }
