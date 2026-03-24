import os
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # ─── App ────────────────────────────────────────────────────
    APP_NAME: str = "PathPilot AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # ─── Security ───────────────────────────────────────────────
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    # ─── Database ── ★ PRIMARY DATABASE CONNECTION ★ ──────────
    # Default: SQLite (no setup needed). Switch to PostgreSQL in .env:
    #   DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/pathpilot_db
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite+aiosqlite:///./pathpilot.db",
    )

    # ─── Vector Database ── ★ VECTOR DB CONNECTION ★ ──────────
    # ChromaDB persists embeddings to this local directory
    CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
    CHROMA_HOST: str = os.getenv("CHROMA_HOST", "")
    CHROMA_PORT: int = int(os.getenv("CHROMA_PORT", "8000"))

    # ─── LLM ── ★ AI ENGINE CONNECTION ★ ──────────────────────
    # LLM_PROVIDER options: groq | ollama | openai
    # Groq is FREE — get key at https://console.groq.com (no credit card)
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "groq")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    GROQ_API_KEYS: list = [k.strip() for k in os.getenv("GROQ_API_KEYS", os.getenv("GROQ_API_KEY", "")).split(",") if k.strip()]
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2")
    
    # Optional Github Copilot fallback
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")

    # ─── Embeddings ─────────────────────────────────────────────
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

    # ─── Redis ──────────────────────────────────────────────────
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # ─── File Uploads ───────────────────────────────────────────
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    ALLOWED_EXTENSIONS: set = {"pdf", "docx", "doc"}

    # ─── CORS ───────────────────────────────────────────────────
    ALLOWED_ORIGINS: list = os.getenv(
        "ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173"
    ).split(",")

    # ─── Interview Scoring Weights ──────────────────────────────
    SCORING_WEIGHTS: dict = {
        "technical": 0.40,
        "communication": 0.30,
        "problem_solving": 0.20,
        "cultural_fit": 0.10,
    }

    # ─── Roadmap Limits ─────────────────────────────────────────
    MAX_ROADMAP_WEEKS: int = 24
    MIN_ROADMAP_WEEKS: int = 4


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
