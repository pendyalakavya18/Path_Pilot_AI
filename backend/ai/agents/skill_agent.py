"""
skill_agent.py — Skill Gap Agent

Analyzes the gap between user skills and company/role requirements.
Uses:
  - ChromaDB RAG to retrieve role requirements
  - LLM for recommendations
  - Embedding similarity for partial skill matching
"""

from ai.llm_engine import llm_engine
from ai.rag_pipeline import rag_pipeline
from ai.knowledge_base import get_company_skills, COMPANIES


GENERIC_ROLE_SKILLS = {
    "software engineer": ["Data Structures", "Algorithms", "System Design", "Python", "SQL"],
    "data scientist": ["Python", "Machine Learning", "Statistics", "SQL", "Data Visualization"],
    "frontend developer": ["JavaScript", "React", "CSS", "HTML", "TypeScript"],
    "backend developer": ["Python", "Java", "System Design", "SQL", "Docker"],
    "devops engineer": ["Docker", "Kubernetes", "CI/CD", "Linux", "AWS"],
    "ml engineer": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "Statistics"],
    "product manager": ["Product Strategy", "Agile", "User Research", "Data Analysis", "Roadmapping"],
    "ui/ux designer": ["Figma", "User Research", "Wireframing", "Prototyping", "Usability Testing"],
    "data analyst": ["SQL", "Excel", "Data Visualization", "Tableau", "Statistics"],
    "marketing manager": ["Digital Marketing", "SEO", "Content Strategy", "Analytics", "Campaign Management"],
    "business analyst": ["Requirements Gathering", "Data Analysis", "Process Modeling", "SQL", "Stakeholder Management"],
}


class SkillAgent:

    async def analyze(self, user_skills: list[str], company: str, role: str) -> dict:
        """
        Compute skill gap. Returns:
        {
          required_skills, user_skills, missing_skills [{skill, priority}],
          existing_skills, recommendations, match_score, company, role
        }
        """
        # 1. Fetch LIVE real-time requirements from WebAgent
        print(f"[SkillAgent] Fetching LIVE real-time requirements for {role} at {company} from WebAgent...")
        required = []
        from ai.agents.web_agent import web_agent
        try:
            required = await web_agent.get_company_requirements(company, role)
        except Exception as e:
            print(f"[SkillAgent] Web search failed ({e}), falling back to RAG/database.")

        # 2. Try to get required skills from Knowledge Base (RAG) if Web search fails
        if not required or len(required) < 2:
            print(f"[SkillAgent] Checking Knowledge Base (RAG) for {role} at {company}...")
            rag_docs = await rag_pipeline.search(
                query=f"{role} at {company} required skills",
                collection="company_requirements",
                top_k=3,
            )
            
            if rag_docs and rag_docs[0].get("score", 0) > 0.75:
                print(f"[SkillAgent] Found strong RAG match: {rag_docs[0].get('score')}")
                skills_text = rag_docs[0].get("metadata", {}).get("skills", "")
                required = [s.strip() for s in skills_text.split(",") if s.strip()]

        # 3. Last resorts
        if not required or len(required) < 2:
            required = get_company_skills(company, role)
        
        if not required:
            required = GENERIC_ROLE_SKILLS.get(role.lower(), ["Core Fundamentals", "Domain Knowledge", "Tools & Frameworks"])

        # 2. Compute gap
        user_lower = {s.lower() for s in user_skills}
        missing = []
        existing = []
        for skill in required:
            if skill.lower() in user_lower:
                existing.append(skill)
            else:
                # Top 3 skills in the required list are considered HIGH priority
                priority = "HIGH" if required.index(skill) < 3 else "MEDIUM"
                missing.append({"skill": skill, "priority": priority})

        # 3. Compute match score
        match_score = round(len(existing) / max(len(required), 1) * 100, 1)

        # 4. LLM recommendations
        recommendations = await self._get_recommendations(
            missing_skills=missing,
            existing_skills=existing,
            company=company,
            role=role,
        )

        return {
            "company": company,
            "role": role,
            "required_skills": required,
            "user_skills": user_skills,
            "missing_skills": missing,
            "existing_skills": existing,
            "recommendations": recommendations,
            "match_score": match_score,
        }

    async def _get_recommendations(
        self,
        missing_skills: list[dict],
        existing_skills: list[str],
        company: str,
        role: str,
    ) -> list[dict]:
        if not missing_skills:
            return [{"action": "Focus on mock interviews and revision", "priority": "LOW"}]

        # Retrieve learning resources from RAG
        top_missing = [m["skill"] for m in missing_skills[:5]]
        context = await rag_pipeline.search(
            query=" ".join(top_missing),
            collection="learning_resources",
            top_k=8,
        )

        prompt = f"""
A student targeting {role} at {company} has these skill gaps:
Missing skills: {[m['skill'] for m in missing_skills]}
Existing skills: {existing_skills}

Available learning resources:
{chr(10).join(d.get('document', '') for d in context[:5])}

Generate 5 concrete, actionable studying steps. 
Return ONLY a valid JSON array of strings (no objects, just strings). Example:
[
  "Practice 50 LeetCode medium problems on Arrays and Strings",
  "Study System Design from Grokking the System Design Interview",
  "Complete the Neetcode 150 list"
]
"""
        raw = await llm_engine._call(prompt)
        recs = llm_engine._parse_json(raw, list)
        if isinstance(recs, list) and recs and isinstance(recs[0], str):
             # Frontend expects simple string recommendations
             return recs
             
        # Fallback
        return [f"Study {m['skill']} using available resources" for m in missing_skills[:5]]
