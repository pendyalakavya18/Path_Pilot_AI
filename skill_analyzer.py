from ai_engine import OllamaEngine
from embeddings import EmbeddingGenerator
from knowledge_base import get_company_skills

# Skills the AI should try to infer for unknown company+role combos
GENERIC_ROLE_SKILLS = {
    'software engineer': ['Python', 'Algorithms', 'Data Structures', 'System Design', 'SQL', 'Git'],
    'data scientist': ['Python', 'Machine Learning', 'Statistics', 'SQL', 'Data Analysis', 'TensorFlow'],
    'data analyst': ['SQL', 'Python', 'Excel', 'Data Visualization', 'Statistics', 'Power BI'],
    'frontend engineer': ['JavaScript', 'React', 'TypeScript', 'HTML', 'CSS', 'Web Performance'],
    'backend engineer': ['Python', 'Java', 'Databases', 'REST APIs', 'Microservices', 'System Design'],
    'devops engineer': ['Docker', 'Kubernetes', 'CI/CD', 'Linux', 'AWS', 'Terraform'],
    'ml engineer': ['Python', 'Machine Learning', 'Deep Learning', 'MLOps', 'TensorFlow', 'PyTorch'],
    'full stack developer': ['JavaScript', 'React', 'Node.js', 'SQL', 'REST APIs', 'HTML/CSS'],
    'mobile engineer': ['Kotlin', 'Swift', 'React Native', 'Mobile Architecture', 'CI/CD'],
    'data engineer': ['Python', 'SQL', 'Spark', 'ETL', 'Cloud', 'Data Warehousing'],
}

def _infer_skills_for_role(role):
    """Return a reasonable skill set for a role that isn't in the knowledge base."""
    role_lower = role.lower()
    for key, skills in GENERIC_ROLE_SKILLS.items():
        if key in role_lower or any(word in role_lower for word in key.split()):
            return skills
    # Generic fallback
    return ['Python', 'Algorithms', 'Data Structures', 'System Design', 'SQL', 'Communication']


class SkillAnalyzer:
    def __init__(self):
        self.ai_engine = OllamaEngine()
        self.embedding_gen = EmbeddingGenerator()
    
    def analyze_gap(self, user_skills, company, role):
        # Try knowledge base first
        required_skills = get_company_skills(company, role)

        # If not found in knowledge base, infer from generic role map
        if not required_skills:
            required_skills = _infer_skills_for_role(role)
        
        user_skills_lower = [s.lower() for s in user_skills]
        required_skills_lower = [s.lower() for s in required_skills]
        
        matched_skills = list(set(user_skills_lower) & set(required_skills_lower))
        missing_skills = list(set(required_skills_lower) - set(user_skills_lower))
        
        gap_percentage = (len(missing_skills) / len(required_skills)) * 100 if required_skills else 0
        
        ai_analysis = self.ai_engine.analyze_skill_gap(user_skills, required_skills)
        
        return {
            'company': company,
            'role': role,
            'required_skills': required_skills,
            'user_skills': user_skills,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'gap_percentage': round(gap_percentage, 2),
            'ai_recommendations': ai_analysis
        }
    
    def compute_skill_match_score(self, user_skills, required_skills):
        if not required_skills:
            return 0.0
        
        user_embeddings = self.embedding_gen.encode(user_skills)
        required_embeddings = self.embedding_gen.encode(required_skills)
        
        if len(user_embeddings.shape) == 1:
            user_embeddings = user_embeddings.reshape(1, -1)
        if len(required_embeddings.shape) == 1:
            required_embeddings = required_embeddings.reshape(1, -1)
        
        similarities = []
        for req_emb in required_embeddings:
            max_sim = 0
            for user_emb in user_embeddings:
                sim = self.embedding_gen.compute_similarity(user_emb, req_emb)
                max_sim = max(max_sim, sim)
            similarities.append(max_sim)
        
        avg_similarity = sum(similarities) / len(similarities) if similarities else 0
        return round(avg_similarity * 100, 2)
    
    def prioritize_skills(self, missing_skills, role):
        if not missing_skills:
            return []
        
        core_skills = ['Algorithms', 'Data Structures', 'System Design', 'Python', 'Java']
        
        priority_list = []
        for skill in missing_skills:
            priority = 2
            if any(core in skill for core in core_skills):
                priority = 1
            priority_list.append({'skill': skill, 'priority': priority})
        
        priority_list.sort(key=lambda x: x['priority'])
        return [item['skill'] for item in priority_list]
