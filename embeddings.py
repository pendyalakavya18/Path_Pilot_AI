import numpy as np
from sentence_transformers import SentenceTransformer
from config import Config

class EmbeddingGenerator:
    def __init__(self):
        self.model = SentenceTransformer(Config.EMBEDDING_MODEL)
    
    def encode(self, text):
        if isinstance(text, str):
            return self.model.encode(text, convert_to_numpy=True)
        elif isinstance(text, list):
            return self.model.encode(text, convert_to_numpy=True)
        else:
            raise ValueError("Input must be string or list of strings")
    
    def compute_similarity(self, embedding1, embedding2):
        return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
    
    def encode_user_profile(self, skills, goals, experience):
        profile_text = f"Skills: {', '.join(skills)}. Goals: {goals}. Experience: {experience}"
        return self.encode(profile_text)
    
    def encode_job_requirements(self, role, company, required_skills):
        job_text = f"Role: {role} at {company}. Required skills: {', '.join(required_skills)}"
        return self.encode(job_text)
