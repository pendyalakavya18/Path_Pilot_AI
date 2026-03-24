import asyncio
from backend.ai.llm_engine import llm_engine

async def test_llm():
    print("Testing LLM generation...")
    roadmap = await llm_engine.generate_roadmap(
        role="Product Manager",
        company="Google",
        weeks=4,
        current_skills=["Agile"],
        missing_skills=["Product Strategy"],
        context=[]
    )
    print("LLM Output:", roadmap)

if __name__ == "__main__":
    asyncio.run(test_llm())
