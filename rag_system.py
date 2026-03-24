import numpy as np
import faiss
from embeddings import EmbeddingGenerator
from knowledge_base import LEARNING_RESOURCES, COMPANIES
import json

class RAGSystem:
    def __init__(self):
        self.embedding_gen = EmbeddingGenerator()
        self.index = None
        self.documents = []
        self.document_metadata = []
        self._build_knowledge_base()
    
    def _build_knowledge_base(self):
        documents = []
        metadata = []
        
        for skill, resources in LEARNING_RESOURCES.items():
            for resource in resources:
                doc_text = f"{skill}: {resource['title']} - {resource['type']}"
                documents.append(doc_text)
                metadata.append({
                    'skill': skill,
                    'title': resource['title'],
                    'url': resource['url'],
                    'type': resource['type']
                })
        
        for company, data in COMPANIES.items():
            for role, skills in data['roles'].items():
                doc_text = f"{company} {role} requires: {', '.join(skills)}"
                documents.append(doc_text)
                metadata.append({
                    'company': company,
                    'role': role,
                    'skills': skills,
                    'type': 'job_requirement'
                })
        
        self.documents = documents
        self.document_metadata = metadata
        
        embeddings = self.embedding_gen.encode(documents)
        
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings.astype('float32'))
    
    def search(self, query, top_k=5):
        query_embedding = self.embedding_gen.encode(query)
        query_embedding = query_embedding.reshape(1, -1).astype('float32')
        
        distances, indices = self.index.search(query_embedding, top_k)
        
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.documents):
                results.append({
                    'document': self.documents[idx],
                    'metadata': self.document_metadata[idx],
                    'score': float(1 / (1 + distance))
                })
        
        return results
    
    def get_resources_for_skill(self, skill, top_k=3):
        results = self.search(skill, top_k=top_k)
        resources = []
        for result in results:
            if result['metadata'].get('type') != 'job_requirement':
                resources.append(result['metadata'])
        return resources
    
    def get_similar_roles(self, role, company=None, top_k=3):
        query = f"{role} at {company}" if company else role
        results = self.search(query, top_k=top_k)
        roles = []
        for result in results:
            if result['metadata'].get('type') == 'job_requirement':
                roles.append(result['metadata'])
        return roles
