import asyncio
from ai.llm_engine import llm_engine
from ai.rag_pipeline import rag_pipeline
import traceback

async def test_llm():
    print("Testing LLM Engine...")
    try:
        res = await llm_engine._call("Say exactly 'HELLO WORLD'")
        print(f"LLM Response: {res}")
        if not res:
            print("LLM CALL FAILED! The response was empty.")
    except Exception as e:
        print("LLM Exception:", e)
        traceback.print_exc()

async def test_rag():
    print("\nTesting RAG Pipeline...")
    try:
        await rag_pipeline.initialize()
        print(f"RAG Ready: {rag_pipeline._ready}")
        res = await rag_pipeline.search("Data Structures", collection="learning_resources", top_k=2)
        print(f"RAG Results: {len(res)} found")
        for r in res:
            print(f" - {r.get('metadata', {}).get('title', 'Unknown')} | {r.get('metadata', {}).get('url', 'No URL')}")
    except Exception as e:
        print("RAG Exception:", e)
        traceback.print_exc()

async def main():
    await test_llm()
    await test_rag()

if __name__ == "__main__":
    asyncio.run(main())
