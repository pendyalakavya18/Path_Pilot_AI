# PathPilot AI — Full System Architecture

## Table of Contents
1. [System Overview](#1-system-overview)
2. [Technology Stack](#2-technology-stack)
3. [Folder Structure](#3-folder-structure)
4. [Database Schema](#4-database-schema)
5. [API Endpoints](#5-api-endpoints)
6. [AI Architecture](#6-ai-architecture)
7. [RAG Pipeline](#7-rag-pipeline)
8. [Agent Architecture](#8-agent-architecture)
9. [Database Connection Guide](#9-database-connection-guide)
10. [Implementation Plan](#10-implementation-plan)
11. [Deployment Guide](#11-deployment-guide)

---

## 1. System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         PATHPILOT AI                                │
│                  AI-Powered Career Preparation Platform             │
└─────────────────────────────────────────────────────────────────────┘

  ┌─────────────┐      HTTPS/REST       ┌──────────────────────────┐
  │             │ ─────────────────────▶│                          │
  │  FRONTEND   │                       │   BACKEND (FastAPI)      │
  │  (React +   │ ◀─────────────────────│   backend/main.py        │
  │   Vite)     │      JSON responses   │                          │
  │             │                       └──────────┬───────────────┘
  │ frontend/   │                                  │
  └─────────────┘                       ┌──────────▼───────────────┐
                                        │     SERVICE LAYER         │
                                        │  auth / roadmap / test /  │
                                        │  interview / resume /     │
                                        │  eligibility / progress   │
                                        └──────────┬───────────────┘
                                                   │
                              ┌────────────────────┼──────────────────┐
                              │                    │                  │
                    ┌─────────▼──────┐  ┌──────────▼──────┐  ┌───────▼───────┐
                    │  PostgreSQL DB │  │   ChromaDB       │  │   LLM Engine  │
                    │  (users, road- │  │   (vector store, │  │   OpenAI /    │
                    │  maps, tests,  │  │    RAG docs,     │  │   Ollama      │
                    │  interviews)   │  │    embeddings)   │  │               │
                    │  ← PRIMARY DB  │  │  ← VECTOR DB     │  │  ← AI ENGINE  │
                    └────────────────┘  └─────────────────┘  └───────────────┘
```

---

## 2. Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React 18 + Vite | SPA, fast build |
| **Styling** | Tailwind CSS | Utility-first CSS |
| **State** | Zustand | Lightweight state management |
| **HTTP Client** | Axios | API calls with interceptors |
| **Routing** | React Router v6 | Client-side routing |
| **Backend** | FastAPI (Python) | Async REST API |
| **Auth** | JWT (python-jose) + bcrypt | Secure auth |
| **ORM** | SQLAlchemy 2.0 (async) | Database abstraction |
| **Migrations** | Alembic | DB schema versioning |
| **Primary DB** | PostgreSQL 15 | Relational data store |
| **Vector DB** | ChromaDB | Embeddings + semantic search |
| **LLM** | OpenAI gpt-4o-mini / Ollama | AI generation |
| **Embeddings** | sentence-transformers | Text embeddings |
| **Resume Parse** | PyMuPDF + pdfplumber | PDF text extraction |
| **Cache** | Redis (optional) | Session/response caching |
| **Container** | Docker + docker-compose | Local dev environment |

---

## 3. Folder Structure

```
PathPilotAI_Project/
│
├── backend/                         ← Python FastAPI Backend
│   ├── main.py                      ← App entry point, register routers
│   ├── config.py                    ← All app settings (reads .env)
│   ├── database.py                  ← ★ DATABASE CONNECTION POINT ★
│   ├── requirements.txt
│   ├── .env.example                 ← Copy to .env and fill in values
│   │
│   ├── models/                      ← SQLAlchemy ORM models (DB tables)
│   │   ├── user.py                  ← users, user_skills, resumes
│   │   ├── roadmap.py               ← roadmaps, roadmap_progress
│   │   ├── test.py                  ← practice_tests
│   │   └── interview.py             ← interviews
│   │
│   ├── schemas/                     ← Pydantic request/response schemas
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── roadmap.py
│   │   ├── test.py
│   │   └── interview.py
│   │
│   ├── routers/                     ← FastAPI route handlers
│   │   ├── auth.py                  ← POST /auth/register, /auth/login
│   │   ├── users.py                 ← GET/PUT /users/me, /users/profile
│   │   ├── roadmaps.py              ← POST /roadmaps/generate, GET /roadmaps
│   │   ├── tests.py                 ← POST /tests/generate, /tests/submit
│   │   ├── interviews.py            ← POST /interviews/start, /evaluate
│   │   ├── resume.py                ← POST /resume/upload, /resume/analyze
│   │   ├── companies.py             ← GET /companies, /companies/{id}/roles
│   │   ├── eligibility.py           ← POST /eligibility/check
│   │   └── progress.py              ← GET /progress
│   │
│   ├── services/                    ← Business logic
│   │   ├── auth_service.py
│   │   ├── roadmap_service.py
│   │   ├── skill_service.py
│   │   ├── interview_service.py
│   │   ├── test_service.py
│   │   ├── resume_service.py
│   │   └── eligibility_service.py
│   │
│   └── ai/                          ← AI components
│       ├── llm_engine.py            ← ★ LLM CONNECTION POINT ★
│       ├── rag_pipeline.py          ← ★ VECTOR DB CONNECTION POINT ★
│       ├── embeddings.py
│       ├── knowledge_base.py
│       └── agents/
│           ├── roadmap_agent.py     ← Monitors progress, adapts roadmap
│           ├── interview_agent.py   ← Manages interview conversation flow
│           └── skill_agent.py       ← Analyzes skills, finds gaps
│
├── frontend/                        ← React + Vite Frontend
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── main.jsx                 ← React entry point
│       ├── App.jsx                  ← Routes definition
│       ├── api/
│       │   ├── client.js            ← ★ FRONTEND API CONNECTION POINT ★
│       │   ├── auth.js
│       │   ├── roadmap.js
│       │   ├── interview.js
│       │   └── test.js
│       ├── stores/
│       │   └── authStore.js         ← Zustand global auth state
│       ├── utils/
│       │   └── auth.js              ← Token helpers
│       ├── components/
│       │   ├── Navbar.jsx
│       │   └── ProtectedRoute.jsx
│       └── pages/
│           ├── Login.jsx
│           ├── Register.jsx
│           ├── Dashboard.jsx
│           ├── RoadmapCreate.jsx
│           ├── RoadmapView.jsx
│           ├── MockInterview.jsx
│           ├── PracticeTest.jsx
│           ├── SkillGap.jsx
│           └── Profile.jsx
│
└── docker-compose.yml               ← Spins up PostgreSQL + ChromaDB + Redis
```

---

## 4. Database Schema

### PostgreSQL Tables

```sql
-- ════════════════════════════════════════
-- TABLE: users
-- ════════════════════════════════════════
CREATE TABLE users (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email         VARCHAR(255) UNIQUE NOT NULL,
    name          VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    cgpa          FLOAT,
    branch        VARCHAR(100),
    graduation_year INTEGER,
    experience_years FLOAT DEFAULT 0.0,
    target_company VARCHAR(100),
    target_role    VARCHAR(100),
    is_active     BOOLEAN DEFAULT TRUE,
    created_at    TIMESTAMPTZ DEFAULT NOW(),
    updated_at    TIMESTAMPTZ DEFAULT NOW()
);

-- ════════════════════════════════════════
-- TABLE: user_skills
-- ════════════════════════════════════════
CREATE TABLE user_skills (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id       UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    skill_name    VARCHAR(100) NOT NULL,
    proficiency   VARCHAR(20) DEFAULT 'beginner',  -- beginner/intermediate/advanced
    UNIQUE(user_id, skill_name)
);

-- ════════════════════════════════════════
-- TABLE: resumes
-- ════════════════════════════════════════
CREATE TABLE resumes (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id       UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    filename      VARCHAR(255),
    file_path     VARCHAR(500),
    parsed_text   TEXT,
    extracted_skills JSONB DEFAULT '[]',
    analysis_result  JSONB DEFAULT '{}',
    created_at    TIMESTAMPTZ DEFAULT NOW()
);

-- ════════════════════════════════════════
-- TABLE: roadmaps
-- ════════════════════════════════════════
CREATE TABLE roadmaps (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id       UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    company       VARCHAR(100) NOT NULL,
    role          VARCHAR(100) NOT NULL,
    total_weeks   INTEGER NOT NULL,
    current_week  INTEGER DEFAULT 0,
    status        VARCHAR(20) DEFAULT 'active',  -- active/completed/paused
    weekly_plan   JSONB NOT NULL DEFAULT '[]',
    skill_gap     JSONB DEFAULT '{}',
    created_at    TIMESTAMPTZ DEFAULT NOW(),
    updated_at    TIMESTAMPTZ DEFAULT NOW()
);

-- ════════════════════════════════════════
-- TABLE: roadmap_progress
-- ════════════════════════════════════════
CREATE TABLE roadmap_progress (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    roadmap_id    UUID NOT NULL REFERENCES roadmaps(id) ON DELETE CASCADE,
    week_number   INTEGER NOT NULL,
    topic         VARCHAR(200) NOT NULL,
    completed     BOOLEAN DEFAULT FALSE,
    completed_at  TIMESTAMPTZ,
    UNIQUE(roadmap_id, week_number, topic)
);

-- ════════════════════════════════════════
-- TABLE: practice_tests
-- ════════════════════════════════════════
CREATE TABLE practice_tests (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id       UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    roadmap_id    UUID REFERENCES roadmaps(id) ON DELETE SET NULL,
    topic         VARCHAR(200) NOT NULL,
    questions     JSONB NOT NULL DEFAULT '[]',
    user_answers  JSONB DEFAULT '[]',
    score         FLOAT,
    total_questions INTEGER,
    performance_level VARCHAR(50),
    taken_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ════════════════════════════════════════
-- TABLE: interviews
-- ════════════════════════════════════════
CREATE TABLE interviews (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id       UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    topic         VARCHAR(200) NOT NULL,
    difficulty    VARCHAR(20) DEFAULT 'medium',
    questions     JSONB NOT NULL DEFAULT '[]',
    evaluations   JSONB DEFAULT '[]',
    overall_score FLOAT,
    technical_score FLOAT,
    communication_score FLOAT,
    confidence_score FLOAT,
    feedback      TEXT,
    strengths     JSONB DEFAULT '[]',
    improvements  JSONB DEFAULT '[]',
    created_at    TIMESTAMPTZ DEFAULT NOW()
);

-- ════════════════════════════════════════
-- TABLE: skill_gap_analyses
-- ════════════════════════════════════════
CREATE TABLE skill_gap_analyses (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id       UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    company       VARCHAR(100),
    role          VARCHAR(100),
    required_skills  JSONB DEFAULT '[]',
    user_skills      JSONB DEFAULT '[]',
    missing_skills   JSONB DEFAULT '[]',
    existing_skills  JSONB DEFAULT '[]',
    recommendations  JSONB DEFAULT '[]',
    match_score   FLOAT DEFAULT 0.0,
    created_at    TIMESTAMPTZ DEFAULT NOW()
);
```

### ChromaDB Collections (Vector Database)

| Collection | Contents | Used For |
|---|---|---|
| `learning_resources` | Docs: title + URL + description | RAG: finding best resources for a topic |
| `interview_questions` | Question bank by topic + difficulty | RAG: generating relevant questions |
| `company_requirements` | Role + company + required skills | RAG: matching user to company needs |
| `roadmap_templates` | Past successful roadmaps | RAG: generating new roadmaps |

---

## 5. API Endpoints

### Authentication
| Method | Path | Description |
|--------|------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login, returns JWT tokens |
| POST | `/auth/refresh` | Refresh access token |
| POST | `/auth/logout` | Invalidate refresh token |

### Users
| Method | Path | Description |
|--------|------|-------------|
| GET | `/users/me` | Get current user profile |
| PUT | `/users/me` | Update profile |
| PUT | `/users/me/skills` | Update user skills |

### Roadmaps
| Method | Path | Description |
|--------|------|-------------|
| POST | `/roadmaps/generate` | Generate AI roadmap |
| GET | `/roadmaps` | List user's roadmaps |
| GET | `/roadmaps/{id}` | Get roadmap by ID |
| PUT | `/roadmaps/{id}/progress` | Mark topic as complete |
| GET | `/roadmaps/{id}/week/{n}` | Get week details |
| POST | `/roadmaps/{id}/adapt` | Trigger roadmap adaptation |

### Practice Tests
| Method | Path | Description |
|--------|------|-------------|
| POST | `/tests/generate` | Generate topic-specific test |
| POST | `/tests/submit` | Submit answers, get score |
| GET | `/tests` | List user's test history |
| GET | `/tests/{id}` | Get test details + results |

### Interviews
| Method | Path | Description |
|--------|------|-------------|
| POST | `/interviews/start` | Start new interview session |
| POST | `/interviews/{id}/answer` | Submit answer, get next question |
| POST | `/interviews/{id}/evaluate` | Evaluate full interview |
| GET | `/interviews` | List user's interviews |
| GET | `/interviews/{id}` | Get interview + feedback |

### Resume
| Method | Path | Description |
|--------|------|-------------|
| POST | `/resume/upload` | Upload PDF resume |
| POST | `/resume/analyze` | Analyze resume, extract skills |
| GET | `/resume` | Get latest resume analysis |

### Companies
| Method | Path | Description |
|--------|------|-------------|
| GET | `/companies` | List all companies |
| GET | `/companies/{name}/roles` | Get roles for a company |
| GET | `/companies/{name}/requirements` | Get eligibility requirements |

### Eligibility
| Method | Path | Description |
|--------|------|-------------|
| POST | `/eligibility/check` | Check if user eligible for company |
| GET | `/eligibility/suggestions` | Get companies user is eligible for |

### Progress
| Method | Path | Description |
|--------|------|-------------|
| GET | `/progress` | Full progress dashboard data |
| GET | `/progress/readiness` | Overall readiness score |

---

## 6. AI Architecture

```
┌──────────────────────────────────────────────────────────┐
│                     AI ENGINE LAYER                      │
│                   backend/ai/                            │
└──────────────────────────────────────────────────────────┘

  ┌─────────────────┐    ┌──────────────┐    ┌────────────────┐
  │   LLM Engine    │    │  RAG Pipeline│    │   Embeddings   │
  │  llm_engine.py  │    │rag_pipeline.│    │ embeddings.py  │
  │                 │    │     py       │    │                │
  │ • OpenAI API    │    │ • ChromaDB   │    │ • HuggingFace  │
  │ • Ollama local  │    │ • Semantic   │    │   MiniLM-L6-v2 │
  │ • Fallback      │    │   search     │    │ • Cosine sim   │
  └────────┬────────┘    └──────┬───────┘    └────────┬───────┘
           │                   │                      │
           └───────────────────┼──────────────────────┘
                               │
            ┌──────────────────▼───────────────────┐
            │              AGENTS                  │
            └──────────────────────────────────────┘
            
  ┌──────────────────┐  ┌─────────────────┐  ┌───────────────┐
  │  RoadmapAgent    │  │ InterviewAgent  │  │  SkillAgent   │
  │                  │  │                 │  │               │
  │ • Monitors week  │  │ • Manages conv  │  │ • Gap analysis│
  │   completion     │  │   state         │  │ • Priority    │
  │ • Detects lag    │  │ • Asks follow-  │  │   ranking     │
  │ • Adapts plan    │  │   up questions  │  │ • Resume parse│
  │ • Alerts user    │  │ • Evaluates     │  │               │
  └──────────────────┘  │   real-time     │  └───────────────┘
                        └─────────────────┘
```

---

## 7. RAG Pipeline

```
                     RAG PIPELINE
                  backend/ai/rag_pipeline.py

Step 1: INDEXING (happens at startup)
─────────────────────────────────────
  Knowledge Sources              ChromaDB Collections
  ─────────────────              ────────────────────
  knowledge_base.py   ────────▶  learning_resources
  Interview question  ────────▶  interview_questions
  banks               ────────▶  company_requirements
  Company requirements────────▶  roadmap_templates

Step 2: QUERYING (at request time)
──────────────────────────────────
  User Query
      │
      ▼
  Embed with sentence-transformers
      │
      ▼
  ChromaDB similarity search (top_k=5)
      │
      ▼
  Retrieved Documents + Metadata
      │
      ▼
  Build Augmented Prompt:
  "Given this context: {docs}
   Answer: {user_query}"
      │
      ▼
  LLM generates response
      │
      ▼
  Structured JSON output

Step 3: USED IN
───────────────
  • Roadmap generation → retrieves company-specific resources
  • Interview questions → retrieves topic-specific question bank
  • Skill gap analysis → retrieves role requirements
  • Practice tests → retrieves topic material for question generation
```

---

## 8. Agent Architecture

### RoadmapAgent (Progress Monitor)
```
Trigger: Called daily / on login
  ↓
1. Load user's active roadmap
2. Calculate expected_week = (days_since_start / 7)
3. Compare with actual current_week
4. If lag > 1 week:
     → Compress remaining topics
     → Increase hours_per_day
     → Send notification
5. If performance_score < 5/10:
     → Add revision topics to next week
     → Suggest remedial resources
6. Save updated roadmap to DB
```

### InterviewAgent (Conversation Manager)
```
State Machine:
  IDLE → STARTED → QUESTIONING → FOLLOW_UP → EVALUATING → COMPLETE

On start:
  → Generate N questions using RAG + LLM
  → Store in session (DB)

On each answer:
  → Evaluate answer quality (LLM)
  → Decide: follow-up needed? (score < 6)
  → If yes: generate follow-up question
  → If no: move to next question
  → Store evaluation

On complete:
  → Aggregate all evaluations
  → Generate overall feedback
  → Calculate scores: technical, communication, confidence
  → Store to interviews table
```

### SkillAgent (Gap Analyzer)
```
On resume upload:
  → Extract text (PyMuPDF)
  → LLM extracts skill list
  → Store to user_skills table

On gap analysis request:
  → Get required skills from ChromaDB (company + role)
  → Compare with user skills (embedding similarity)
  → Classify: missing / existing / partial
  → Prioritize missing skills:
       HIGH: core skills not present
       MEDIUM: partial knowledge
       LOW: existing but needs revision
  → Generate learning recommendations
  → Update roadmap if one exists
```

---

## 9. Database Connection Guide

### WHERE TO CONNECT THE DATABASE

#### 1. Primary Database (PostgreSQL)
**File:** `backend/database.py`  
**Variable:** `DATABASE_URL` in `backend/.env`

```
DATABASE_URL=postgresql+asyncpg://USER:PASSWORD@HOST:PORT/DBNAME
```

**For local dev (docker-compose):**
```
DATABASE_URL=postgresql+asyncpg://pathpilot_user:pathpilot_pass@localhost:5432/pathpilot_db
```

**For production (Render/Railway/Supabase):**
```
DATABASE_URL=postgresql+asyncpg://user:pass@aws-region.render.com:5432/pathpilot_prod
```

#### 2. Vector Database (ChromaDB)
**File:** `backend/ai/rag_pipeline.py`  
**Variable:** `CHROMA_PERSIST_DIR` in `backend/.env`

```
CHROMA_PERSIST_DIR=./chroma_db          # local persistent storage
```

For a hosted ChromaDB server:
```
CHROMA_HOST=your-chroma-server.com
CHROMA_PORT=8000
```

#### 3. LLM Connection
**File:** `backend/ai/llm_engine.py`  
**Variables in `backend/.env`:**

```
LLM_PROVIDER=openai                  # or "ollama"
OPENAI_API_KEY=sk-...                # get from platform.openai.com
OPENAI_MODEL=gpt-4o-mini

# OR for local Ollama:
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
```

#### 4. Frontend → Backend Connection
**File:** `frontend/src/api/client.js`  
**Variable:** `VITE_API_BASE_URL` in `frontend/.env`

```
VITE_API_BASE_URL=http://localhost:8000    # local dev
VITE_API_BASE_URL=https://your-api.render.com  # production
```

---

## 10. Implementation Plan

### Phase 1: Foundation (Week 1-2)
- [ ] Set up PostgreSQL with docker-compose
- [ ] Create all database models + run `alembic upgrade head`
- [ ] Implement JWT authentication (register/login/refresh)
- [ ] Create basic user profile CRUD
- [ ] Set up FastAPI with CORS for React frontend
- [ ] Scaffold React app with React Router + Zustand
- [ ] Build Login + Register pages
- [ ] Connect frontend to backend auth APIs

### Phase 2: Core AI Features (Week 3-4)
- [ ] Integrate OpenAI API (or Ollama)
- [ ] Build ChromaDB RAG pipeline with knowledge base
- [ ] Implement company-specific roadmap generation
- [ ] Build skill gap analysis with resume upload
- [ ] Create practice test generation (topic-specific)
- [ ] Connect all to database (persist results)

### Phase 3: Interview System (Week 5-6)
- [ ] Build InterviewAgent with state machine
- [ ] Implement real-time follow-up question logic
- [ ] Build evaluation with multi-dimensional scoring
- [ ] Create interview session persistence
- [ ] Add feedback + improvement suggestions

### Phase 4: Progress & Monitoring (Week 7-8)
- [ ] Build RoadmapAgent for progress monitoring
- [ ] Implement dynamic roadmap adaptation
- [ ] Build progress dashboard with charts
- [ ] Add company eligibility checker
- [ ] Implement notifications for lagging behind

### Phase 5: Polish & Deploy (Week 9-10)
- [ ] Add Redis caching for expensive AI calls
- [ ] Add rate limiting
- [ ] Write tests (pytest for backend, Vitest for frontend)
- [ ] Set up CI/CD pipeline
- [ ] Deploy backend to Render/Railway
- [ ] Deploy frontend to Vercel/Netlify
- [ ] Connect production PostgreSQL (Supabase or Render Postgres)
- [ ] Set all environment variables in production

---

## 11. Deployment Guide

### Backend → Render
1. Push `backend/` to GitHub
2. Create new Web Service on render.com
3. Set Build Command: `pip install -r requirements.txt`
4. Set Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables (DATABASE_URL, SECRET_KEY, OPENAI_API_KEY)

### Frontend → Vercel
1. Push `frontend/` to GitHub
2. Import project on vercel.com
3. Set Root Directory: `frontend`
4. Set Build Command: `npm run build`
5. Set Output Directory: `dist`
6. Add env var: `VITE_API_BASE_URL=https://your-backend.render.com`

### Database → Supabase (Free PostgreSQL)
1. Create project on supabase.com
2. Copy the connection string (use **Transaction pooler** for serverless)
3. Set `DATABASE_URL` in backend environment
4. Run migrations: `alembic upgrade head`
