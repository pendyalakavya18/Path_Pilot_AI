import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask settings
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    DEBUG = FLASK_ENV != 'production'
    
    # Ollama settings (for AI features)
    OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'tinyllama')
    
    # Embedding settings
    EMBEDDING_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'
    
    # Fallback AI when Ollama is unavailable
    USE_FALLBACK_AI = os.getenv('USE_FALLBACK_AI', 'false').lower() == 'true'
    
    # Data storage settings
    DATA_STORE_TYPE = os.getenv('DATA_STORE_TYPE', 'file')  # 'file' or 'memory'
    
    # Roadmap settings
    MAX_ROADMAP_WEEKS = 24
    MIN_ROADMAP_WEEKS = 4
    
    # Interview settings
    INTERVIEW_DIFFICULTIES = ['Easy', 'Medium', 'Hard']
    
    # Scoring weights
    SCORING_WEIGHTS = {
        'technical': 0.4,
        'communication': 0.3,
        'problem_solving': 0.2,
        'cultural_fit': 0.1
    }

