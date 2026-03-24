import asyncio
from database import AsyncSessionLocal
from models.user import User
from services.roadmap_service import generate_roadmap

async def run_test():
    async with AsyncSessionLocal() as db:
        print("Creating user...")
        user = User(id="test_user_id2", email="test2@test.com", password_hash="hash")
        db.add(user)
        try:
            await db.commit()
            await db.refresh(user)
        except Exception as e:
            print("User creation failed, maybe already exists:", e)
            await db.rollback()

        try:
            print("Generating roadmap...")
            roadmap = await generate_roadmap(
                user=user,
                company="Google",
                role="Product Manager",
                weeks=4,
                current_skills=["Agile", "Scrum"],
                db=db
            )
            print("Success:", roadmap.id)
            print("Themes:", [w.get("theme") for w in roadmap.weekly_plan])
        except Exception as e:
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_test())
