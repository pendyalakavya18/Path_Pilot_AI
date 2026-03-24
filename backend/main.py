"""
main.py — FastAPI application entry point

Start locally:  uvicorn main:app --reload --port 8000
Production:     uvicorn main:app --host 0.0.0.0 --port $PORT --workers 4
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import settings
from database import create_tables

# ── Routers ─────────────────────────────────────────────────────────
from routers import auth, users, roadmaps, tests, interviews, resume, companies, eligibility, progress


# ── Lifespan ─────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await create_tables()
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    # Initialize RAG pipeline — optional, skip if chromadb not installed
    try:
        from ai.rag_pipeline import rag_pipeline
        await rag_pipeline.initialize()
    except Exception as e:
        print(f"[WARNING] RAG pipeline not available: {e}")
    yield
    # Shutdown (nothing needed)


# ── App ──────────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered career preparation platform",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ── CORS ─────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Static Files (resumes, uploads) ──────────────────────────────────
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# ── Register Routers ─────────────────────────────────────────────────
app.include_router(auth.router,        prefix="/auth",        tags=["Authentication"])
app.include_router(users.router,       prefix="/users",       tags=["Users"])
app.include_router(roadmaps.router,    prefix="/roadmaps",    tags=["Roadmaps"])
app.include_router(tests.router,       prefix="/tests",       tags=["Practice Tests"])
app.include_router(interviews.router,  prefix="/interviews",  tags=["Interviews"])
app.include_router(resume.router,      prefix="/resume",      tags=["Resume"])
app.include_router(companies.router,   prefix="/companies",   tags=["Companies"])
app.include_router(eligibility.router, prefix="/eligibility", tags=["Eligibility"])
app.include_router(progress.router,    prefix="/progress",    tags=["Progress"])


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "version": settings.APP_VERSION}
