# PathPilot AI — Presentation Guide

## Before You Present

- [ ] Ollama is running (check system tray)
- [ ] `python app.py` is running in terminal
- [ ] Browser open at `http://localhost:5000`
- [ ] Visit `/roadmap/view` at least once (auto-loads the Google SWE demo roadmap)
- [ ] Close unnecessary tabs and notifications

---

## Suggested Flow (15–20 min demo)

### 1. Landing Page — Set the Context (1 min)

Open `http://localhost:5000`. Briefly introduce what PathPilot AI is:

> *"PathPilot is an AI-powered career preparation platform. It generates personalised learning roadmaps, runs mock interviews, and identifies skill gaps — all powered by a locally-hosted AI model with no internet dependency."*

**Key point to highlight:** The AI runs entirely on the local machine using Ollama — no API keys, no internet, no cost.

---

### 2. Dashboard (1–2 min)

Go to `/dashboard`.

- Point out the **stat cards** — Practice Tests, Mock Interviews, Skills Matched
- Mention the **Recent Activity feed** — shows a history of what the user has done
- The **radar chart** gives a performance overview at a glance

> *"This is the command centre — everything the user needs to track their progress."*

---

### 3. Roadmap Creation — Core Feature (4–5 min)

Go to `/roadmap/create`.

- Show the **Saved Roadmaps** section — point out Google SWE, Amazon Backend, Meta Data Scientist
- Click **Google Software Engineer** to load the demo instantly
- This redirects to the full 12-week roadmap view

**On the roadmap view:**
- Walk through the week cards — each shows the focus area, topics, and milestones
- Click **"View Details"** on Week 1
- Show the full breakdown: topics, milestones, and recommended learning resources pulled by the RAG system

> *"The roadmap is generated based on the role and company. Each week has concrete topics to study, milestones to hit, and resources recommended by the AI based on the user's current skills."*

**If asked about AI generation:** You can also show real generation by going back to `/roadmap/create`, typing a company and role, and clicking Generate — note it takes 1–3 minutes since TinyLlama runs locally.

---

### 4. Skill Gap Analysis (3 min)

Go to `/skill-gap`.

- Type any company name (e.g., **Google**) and role (e.g., **Data Analyst**)
- Click **Analyze Skill Gap**
- Show the results:
  - Skill match percentage bar
  - Matched vs missing skills
  - AI-powered priority order for what to learn first
  - Specific resource recommendations

> *"This feature compares the user's current profile skills against what the target role requires — telling them exactly what to focus on."*

**Tip:** Set up a profile with a few skills first (`/profile`) so the matched skills section is non-empty.

---

### 5. Mock Interview (3–4 min)

Go to `/mock-interview`.

- Select topic: **"System Design"** or **"Python"**
- Select difficulty: **Medium**
- Select **3 questions**
- Click **Start Interview**

Walk through one question:
1. Show the question text — note it's specific and technical, not vague
2. Click **"Show Hints"** to reveal hints
3. Type a short answer and click **Submit Response**
4. Show the evaluation scores (Technical, Communication, Problem Solving, Overall)
5. Show the written feedback

> *"The AI evaluates each answer on four dimensions and gives specific written feedback. At the end of the session, there's a full summary with a radar chart of performance."*

---

### 6. Practice Test (2 min)

Go to `/practice-test`.

- Enter a topic (e.g., **"Algorithms"**)
- Start the test — show the multiple-choice questions
- Highlight that questions are AI-generated and topic-specific

> *"Practice tests help reinforce concepts in a quiz format, with immediate scoring."*

---

### 7. Profile Setup (1 min)

Go to `/profile`.

- Show where users enter their name, current skills, experience level, and goals
- These skills feed into the skill gap analysis and roadmap personalisation

---

## Key Technical Points to Mention

| Point | What to say |
|-------|-------------|
| **AI Model** | TinyLlama via Ollama — runs locally, no API key, zero cost |
| **RAG System** | Uses sentence-transformers + FAISS to retrieve relevant learning resources for each skill |
| **No cloud dependency** | Everything runs on the local machine — works offline |
| **Data persistence** | User data saved in local JSON files — survives restarts |
| **Knowledge base** | 20+ companies, 100+ roles, curated interview question templates |

---

## Handling Tough Questions

**"Why TinyLlama and not GPT-4?"**
> *"Intentional — the goal was to build a system that works completely offline and at zero cost. TinyLlama runs on any local machine. A larger model like Llama 3 can be swapped in by just changing one line in the `.env` file."*

**"What if the AI generates bad content?"**
> *"There's a validation layer — the system detects placeholder text and vague responses and either retries or falls back to curated templates from our knowledge base."*

**"How does the RAG system work?"**
> *"User skills and week topics are embedded using sentence-transformers. FAISS does a vector similarity search over our curated resource library to find the most relevant learning material for each topic."*

**"Can it handle any company?"**
> *"Yes — the skill gap and roadmap features accept free-text input for any company. For known companies, we use the knowledge base. For unknown ones, we infer required skills from the role name using a smart fallback map."*

---

## Flow Cheat Sheet

```
Landing (/] → Dashboard (/dashboard)
           → Create Roadmap (/roadmap/create) → Load Google Demo → View Roadmap → View Details (Week 1)
           → Skill Gap (/skill-gap) → Google + Data Analyst → Results
           → Mock Interview (/mock-interview) → System Design, Medium, 3Q → Answer → Evaluation
           → Practice Test (/practice-test) → Algorithms
           → Profile (/profile)
```

---

## Tips

- **Load the demo roadmap before presenting** — visit `/roadmap/view` once so it's pre-cached
- **Pre-fill your profile** with 3–4 skills (Python, SQL, JavaScript) so skill gap results are richer
- **Use "System Design" for mock interview** — it produces the most impressive questions
- **Don't demo real AI roadmap generation live** — it takes 1–3 min; use the saved roadmaps instead
- **Keep the terminal visible on a second screen** — the `[ROADMAP]` and `[WEEK VIEW]` logs make it look impressively technical
