"""
rag_pipeline.py — ★ VECTOR DATABASE CONNECTION POINT ★

Uses Qdrant as the vector store.
On startup, indexes all knowledge base content.
At query time, performs semantic similarity search.

Connect by setting CHROMA_PERSIST_DIR in backend/.env (Reusing the env variable)
"""

from __future__ import annotations
import uuid
try:
    from qdrant_client import QdrantClient
    from qdrant_client.http.models import Distance, VectorParams, PointStruct
    QDRANT_AVAILABLE = True
except ImportError:
    QdrantClient = None
    QDRANT_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SentenceTransformer = None
    SENTENCE_TRANSFORMERS_AVAILABLE = False

from config import settings
from ai.knowledge_base import COMPANIES, LEARNING_RESOURCES, INTERVIEW_QUESTION_TEMPLATES


class RAGPipeline:
    COLLECTIONS = ["learning_resources", "interview_questions", "company_requirements"]

    def __init__(self):
        self._client: QdrantClient | None = None
        self._model: SentenceTransformer | None = None
        self._ready = False

    async def initialize(self):
        """Load embedding model and build Qdrant collections."""
        if not QDRANT_AVAILABLE or not SENTENCE_TRANSFORMERS_AVAILABLE:
            print("[WARNING] qdrant-client or sentence-transformers not installed — RAG features disabled")
            return
            
        self._client = QdrantClient(path=settings.CHROMA_PERSIST_DIR) # Reusing the env var for simplicity
        self._model = SentenceTransformer(settings.EMBEDDING_MODEL)
        
        self._build_learning_resources()
        self._build_interview_questions()
        self._build_company_requirements()
        self._ready = True

    def _embed(self, text: str) -> list[float]:
        return self._model.encode(text).tolist()

    def _get_or_create(self, name: str):
        if not self._client.collection_exists(name):
            self._client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )

    # ── Indexing ─────────────────────────────────────────────────────

    def _build_learning_resources(self):
        name = "learning_resources"
        self._get_or_create(name)
        if self._client.count(name).count > 0: return
        
        points = []
        for skill, resources in LEARNING_RESOURCES.items():
            for i, res in enumerate(resources):
                text = f"{skill}: {res['title']} — {res.get('description', '')}"
                payload = {"document": text, "skill": skill, "title": res["title"], "url": res.get("url", ""), "type": res.get("type", "")}
                points.append(PointStruct(id=str(uuid.uuid4()), vector=self._embed(text), payload=payload))
        if points:
            self._client.upsert(collection_name=name, points=points)

    def _build_interview_questions(self):
        name = "interview_questions"
        self._get_or_create(name)
        if self._client.count(name).count > 0: return
        
        points = []
        for difficulty, topics in INTERVIEW_QUESTION_TEMPLATES.items():
            for topic, questions in topics.items():
                for q in questions:
                    payload = {"document": q, "difficulty": difficulty, "topic": topic}
                    points.append(PointStruct(id=str(uuid.uuid4()), vector=self._embed(q), payload=payload))
        if points:
            self._client.upsert(collection_name=name, points=points)

    def _build_company_requirements(self):
        name = "company_requirements"
        self._get_or_create(name)
        if self._client.count(name).count > 0: return

        points = []
        for company, data in COMPANIES.items():
            for role, skills in data.get("roles", {}).items():
                text = f"{company} {role}: required skills — {', '.join(skills)}"
                payload = {"document": text, "company": company, "role": role, "skills": ", ".join(skills)}
                points.append(PointStruct(id=str(uuid.uuid4()), vector=self._embed(text), payload=payload))
        if points:
            self._client.upsert(collection_name=name, points=points)

    # ── Querying ─────────────────────────────────────────────────────

    async def search(
        self,
        query: str,
        collection: str = "learning_resources",
        top_k: int = 5,
    ) -> list[dict]:
        """
        Semantic search in a Qdrant collection.
        Returns list of {document, metadata, score} dicts.
        """
        if not self._ready:
            return []
        try:
            results = self._client.search(
                collection_name=collection,
                query_vector=self._embed(query),
                limit=top_k
            )
            return [{"document": r.payload.get("document", ""), "metadata": r.payload, "score": round(r.score, 4)} for r in results]
        except Exception:
            return []

    async def add_document(self, collection: str, text: str, metadata: dict, doc_id: str):
        """Add a new document to a collection (e.g., a new roadmap template)."""
        if not self._ready:
            return
        self._get_or_create(collection)
        payload = metadata.copy()
        payload["document"] = text
        self._client.upsert(collection_name=collection, points=[PointStruct(id=str(uuid.uuid4()), vector=self._embed(text), payload=payload)])


# Module-level singleton, initialized in main.py lifespan
rag_pipeline = RAGPipeline()
