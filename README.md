# PathPilot AI - Student Preparation Platform

An AI-powered web platform to help students prepare for their dream tech roles.

## Features
- **Profile & Resume Parsing**: Upload your resume to automatically extract skills.
- **Skill Gap Analysis**: Compare your skills against the requirements for your target role at your target company.
- **AI Roadmaps**: Generate a customized, week-by-week preparation plan.
- **Mock Interviews**: Interactive real-time interviews with an AI Agent evaluating your technical and behavioral skills.
- **Practice Tests**: RAG-powered MCQs targeting the areas you need the most improvement.
- **Analytics Dashboard**: Track your overall readiness score and progress.

## Tech Stack
- Frontend: React + Vite + Tailwind CSS + Recharts
- Backend: Python + FastAPI
- Database: SQLite (via SQLAlchemy)
- Vector DB: Qdrant
- AI/LLM: GitHub Models API / LangGraph

---

## Getting Started

### Prerequisites
- Node.js (for React frontend)
- Python 3.9+ (for FastAPI backend)

### 1. Backend Setup
1. Open a terminal and navigate to the backend directory: `cd backend`
2. Activate your virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
3. Create your `.env` file inside the `backend` folder (already done). Make sure your GitHub API token is set: `OPENAI_API_KEY=your_token_here`.
4. Run the FastAPI development server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

### 2. Frontend Setup
1. Open a new terminal and navigate to the frontend directory: `cd frontend`
2. Install npm dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```

### 3. Usage
Navigate to `http://localhost:5173` in your browser.
Create an account or sign in to start your preparation journey!
