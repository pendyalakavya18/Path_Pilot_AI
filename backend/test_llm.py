import asyncio
from ai.llm_engine import llm_engine

async def main():
    try:
        print("Testing roadmap generation...")
        res = await llm_engine.generate_roadmap(
            role="Product Manager",
            company="Google",
            weeks=4,
            current_skills=[],
            missing_skills=["Product Strategy"],
            context=[]
        )
        print("RESULT:")
        for w in res:
            print(f"Week {w.get('week')}: {w.get('theme')}")
            for d in w.get("days", []):
                print(f"  Day {d.get('day')}: {d.get('topic')}")
    except Exception as e:
        import traceback; traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
