
import asyncio
import os
import sys

# Add current directory to path for imports
sys.path.append(os.getcwd())

from ai.llm_engine import llm_engine
from config import settings

async def debug_roadmap():
    role = "Machine Learning Engineer"
    company = "Google"
    weeks = 4
    current_skills = ["Python", "Linear Algebra"]
    required_skills = ["TensorFlow", "PyTorch", "NLP", "Deep Learning"]
    missing_skills = ["TensorFlow", "PyTorch", "NLP", "Deep Learning"]
    context = []

    print(f"--- Debugging Roadmap Gen for {role} at {company} ---")
    
    # We want to see the RAW output
    # Since llm_engine.generate_roadmap doesn't return raw, we'll recreate the call
    context_str = "\n".join(f"- {d.get('document','')}" for d in context[:8])
    required_str = ", ".join(required_skills[:12]) if required_skills else "General industry standards"
    missing_str = ", ".join(missing_skills[:10]) if missing_skills else "None identified"
    current_str = ", ".join(current_skills[:10]) if current_skills else "None"

    prompt = f"""
Create a {weeks}-week preparation roadmap for a student targeting:
  Company: {company}
  Role: {role}
  
Core requirements for this role at {company} (CRITICAL):
  {required_str}

Candidate Profile:
  Current skills: {current_str}
  Specific gaps (high priority): {missing_str}

Reference resources:
{context_str}

Rules:
- THE ROADMAP MUST PRIORITIZE THE CORE REQUIREMENTS listed above.
- Allocate MORE weeks to missing skills (high priority)
- Week 1 should build foundations, last week should focus on mock interviews
- Each week must be divided into exactly 5 days (e.g., day 1 to day 5)
- Each day must have EXACTLY ONE specific topic
- Topics must be concrete (e.g., "Binary Trees", "Dynamic Programming", not "Study harder")
- hours_per_day should be 2-4

Respond with ONLY a JSON array:
[
  {{
    "week": 1,
    "theme": "Foundational Concepts for {role} at {company}",
    "days": [
      {{"day": 1, "topic": "Specific topic relevant to {required_str}"}},
      ...
    ],
    "hours_per_day": 2,
    "focus": "Building core foundations specifically for {company}'s tech stack"
  }},
  ...
]
"""
    print("Sending prompt to LLM...")
    try:
        raw = await llm_engine._call(prompt)
        print("\n--- RAW LLM OUTPUT ---")
        print(raw)
        print("--- END RAW LLM OUTPUT ---\n")
        
        plan = llm_engine._parse_json(raw, list)
        print(f"Parsed Plan Type: {type(plan)}")
        if isinstance(plan, list):
            print(f"Plan length: {len(plan)}")
            if len(plan) > 0:
                print("First week theme:", plan[0].get("theme"))
            else:
                print("Plan is an empty list!")
        else:
            print("Plan is not a list!")
            
    except Exception as e:
        print(f"Error during LLM call: {e}")

if __name__ == "__main__":
    asyncio.run(debug_roadmap())
