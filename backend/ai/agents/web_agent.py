"""
web_agent.py — Real-Time Web Search Agent for Company Requirements
Uses DuckDuckGo search to retrieve live software engineering requirements for specific companies
and roles, feeding real-world data into the roadmap and skill gap agents.
"""

from duckduckgo_search import DDGS
from ai.llm_engine import llm_engine

class WebAgent:
    def __init__(self):
        self.ddgs = DDGS()

    async def get_company_requirements(self, company: str, role: str) -> list[str]:
        """
        Searches the web for recent interview requirements and required skills for a given company and role.
        Summarizes the search results using the LLM into a list of core critical skills.
        """
        query = f"{company} {role} job requirements required skills site:glassdoor.com OR site:levels.fyi OR site:linkedin.com OR site:indeed.com"
        
        try:
            results = list(self.ddgs.text(query, max_results=5))
            if results:
                context = "\n".join([f"- {r.get('title', '')}: {r.get('body', '')}" for r in results])
            else:
                context = ""
        except Exception as e:
            print(f"[WebAgent] Search failed for {company}: {e}")
            context = ""

        if context:
            prompt = f"""
Based on the following real-time web search results for "{company} {role}":
{context}

Extract the 5 to 7 most critical hard skills, tools, and technical competencies currently required by {company} for this exact role ({role}).
Ignore generic soft skills (like "communication"). Focus strictly on the specific tools, platforms, languages, frameworks, or methodologies relevant to this specific profession.

Respond with ONLY a JSON array of specific skill strings:
[
  "Figma",
  "User Research",
  "Prototyping",
  "Wireframing",
  "Interaction Design"
]
"""
        else:
            prompt = f"""
You are an expert tech recruiter and technical interviewer.
What are the 5 to 7 most critical hard skills, tools, and technical competencies currently required by {company} for the {role} role?
Provide an extremely accurate and real-world answer based on your knowledge of "{company}". Focus strictly on the specific tools, platforms, languages, frameworks, or methodologies relevant to this specific company and profession.

Respond with ONLY a JSON array of specific skill strings:
[
  "AWS",
  "React",
  "Distributed Systems",
  "Python"
]
"""
        raw = await llm_engine._call(prompt)
        skills = llm_engine._parse_json(raw, list)
        
        # Validate output, ensure it's a list of strings
        if isinstance(skills, list) and skills and isinstance(skills[0], str):
            final_skills = skills
        else:
            final_skills = ["Data Structures", "System Design", "Algorithms", "Problem Solving"]
            
        # Store the fetched real-time data into the Knowledge Base (RAG)
        from ai.rag_pipeline import rag_pipeline
        print(f"[WebAgent] Saving fetched live requirements for {company} to RAG Knowledge Base...")
        
        try:
            await rag_pipeline.add_document(
                collection="company_requirements",
                text=f"Live Web Data for {company} {role}: {context}",
                metadata={"company": company, "role": role, "skills": ", ".join(final_skills)},
                doc_id=f"live_{company}_{role}"
            )
        except Exception as e:
            print(f"[WebAgent] Error persisting to RAG: {e}")
            
        return final_skills

# Singleton instance
web_agent = WebAgent()
