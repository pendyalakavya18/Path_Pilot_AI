<div align="center">
  <img src="https://img.shields.io/badge/Status-Active-success.svg" alt="Status">
  <img src="https://img.shields.io/badge/Frontend-React%20%2B%20Vite-blue.svg" alt="Frontend">
  <img src="https://img.shields.io/badge/Backend-FastAPI-green.svg" alt="Backend">
  <img src="https://img.shields.io/badge/AI-Groq%20%7C%20OpenAI%20%7C%20Ollama-purple.svg" alt="AI">
  
  <h1>🚀 PathPilot AI</h1>
  <p><strong>Your Intelligent Co-Pilot for Tech Career Acceleration</strong></p>
</div>

PathPilot AI is a comprehensive, AI-powered student preparation platform designed to bridge the gap between academic learning and industry requirements. By leveraging advanced Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), and intelligent autonomous agents, PathPilot provides highly personalized career guidance, dynamically generated study roadmaps, and hyper-realistic mock interviews.

---

## ✨ Core Features

*   **📄 Intelligent Resume Parsing & Skill Gap Analysis**
    *   Upload your resume to instantly extract existing skills.
    *   Compare your profile against real-world job requirements for your target role and company.
    *   Receive an actionable "Skill Gap" report detailing exactly what you need to learn.

*   **🗺️ Dynamic, Role-Specific Roadmaps**
    *   Generate a customized, week-by-week preparation plan.
    *   Unlike static plans, PathPilot dynamically adjusts topics based on the specific *role* (e.g., Product Manager, Data Scientist, Frontend Developer) instead of just generic programming concepts.
    *   Features an intelligent adaptation agent that compresses or adjusts the schedule if you fall behind.

*   **🎙️ Hyper-Realistic Mock Interviews**
    *   Real-time, interactive audio/text interviews with an AI evaluator.
    *   Receive detailed, granular feedback on 4 dimensions: Technical Accuracy, Communication, Problem Solving, and Cultural Fit.
    *   Dynamic follow-up questions based on your previous answers.

*   **📝 Targeted Practice Tests**
    *   Generate custom Multiple-Choice Questions (MCQs) powered by RAG on specific topics you are currently studying.
    *   Receive instant evaluation and detailed explanations to reinforce learning.

*   **🌐 Live Web Agent (Knowledge Enrichment)**
    *   When local databases lack specific role requirements, the autonomous Web Agent searches the internet for up-to-date industry standards and instantly updates the RAG Knowledge Base.

---

## 🛠️ Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | React, Vite, Tailwind CSS | High-performance, highly responsive, premium SPA UI. |
| **Backend** | Python, FastAPI | Blazing fast async API for handling agent routing and data. |
| **Database** | PostgreSQL & SQLite | Managed PostgreSQL for production, SQLite for local testing. |
| **Vector DB** | ChromaDB (or Qdrant) | Semantic search for RAG pipelines and knowledge retrieval. |
| **LLM Engine** | Groq / OpenAI / Ollama | Multi-provider fallback engine (defaults to ultra-fast Groq). |
| **Agents** | Custom Python Agents | Independent intelligent agents for skills, roadmaps, and web search. |

---

## 🚀 Getting Started

Follow these steps to set up the project locally.

### Prerequisites
*   Node.js (v18+)
*   Python (3.10+)
*   API Keys: Groq (Recommended/Free), OpenAI, or local Ollama.

### 1. Unified Setup (Recommended for Windows)
If you are on Windows, you can use the provided setup scripts:
```bash
# 1. Start the backend (creates venv, installs deps, runs FastAPI)
.\start_backend.bat

# 2. In a new terminal, start the frontend
cd frontend
npm install
npm run dev
```

### 2. Manual Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a Virtual Environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .\.venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Environment Variables:
   Create a `.env` file in the `backend/` directory referencing `.env.example`.
   ```env
   LLM_PROVIDER=groq
   GROQ_API_KEYS=your_groq_api_key_here
   ```
5. Run the Server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

### 3. Manual Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the Development Server:
   ```bash
   npm run dev
   ```

You can now access the application at `http://localhost:5173`.

---

## ☁️ Deployment (Render & Vercel)

PathPilot AI is optimized for high-performance deployment on **Render** (Backend) and **Vercel** (Frontend).

### 1. Backend (Render)
1.  **Connect Repo**: Connect your GitHub repository to Render.
2.  **Web Service**: Render will automatically detect the `render.yaml` file.
3.  **Environment Variables**: Ensure you set `LLM_PROVIDER`, `GROQ_API_KEYS`, `SECRET_KEY`, and `DATABASE_URL` in the Render dashboard.
4.  **Database**: It is highly recommended to use a **Render Managed PostgreSQL** instance for production data persistence.

### 2. Frontend (Vercel)
1.  **Connect Repo**: Import the `frontend/` directory to Vercel.
2.  **Environment Variables**: Set `VITE_API_BASE_URL` to your Render service URL.
3.  **Deploy**: Vercel will build and host your premium UI.

---

## 🧠 Architecture Overview

PathPilot operates on a micro-agent architecture:
*   **Skill Agent**: Analyzes resumes and determines gaps using rule-based metrics and LLM semantic matching.
*   **Roadmap Agent**: Orchestrates RAG context to supply the LLM Engine with necessary topics for dynamic roadmap generation.
*   **Web Agent**: Uses duckduckgo-search and BeautifulSoup to actively scrape the web for missing modern knowledge and saves it to the vector database.
*   **Interview Engine**: Maintains conversational context and parses strict JSON evaluations for user responses.

---

## 🤝 Contributing

Contributions are welcome! If you'd like to improve the AI agents, enhance the UI, or add new interview types:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

<div align="center">
  <p>Built with ❤️ to accelerate tech careers.</p>
</div>
