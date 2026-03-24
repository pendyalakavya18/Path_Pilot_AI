import asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

async def test_llm():
    from backend.ai.llm_engine import llm_engine
    print("Testing LLM Engine...")
    res = await llm_engine._call("Say exactly 'HELLO WORLD'")
    print(f"LLM Response: {res}")
    if not res:
        print("LLM CALL FAILED! Check API key or model.")

async def test_rag():
    from backend.ai.rag_pipeline import rag_pipeline
    print("\nTesting RAG Pipeline...")
    await rag_pipeline.initialize()
    print(f"RAG Ready: {rag_pipeline._ready}")
    res = await rag_pipeline.search("Data Structures", collection="learning_resources", top_k=2)
    print(f"RAG Results: {res}")

async def main():
    await test_llm()
    await test_rag()

if __name__ == "__main__":
    asyncio.run(main())
