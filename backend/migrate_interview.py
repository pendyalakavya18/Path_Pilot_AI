
import asyncio
from database import engine
from sqlalchemy import text

async def migrate_interview_table():
    print("Migrating interview table...")
    async with engine.begin() as conn:
        # Check for company column
        try:
            await conn.execute(text("ALTER TABLE interviews ADD COLUMN company VARCHAR(100)"))
            print("Added 'company' column.")
        except Exception:
            print("'company' column likely exists.")
            
        # Check for role column
        try:
            await conn.execute(text("ALTER TABLE interviews ADD COLUMN role VARCHAR(100)"))
            print("Added 'role' column.")
        except Exception:
            print("'role' column likely exists.")
            
    # Also ensure skill_gap_analyses table exists
    from models.roadmap import SkillGapAnalysis
    from database import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Ensured all tables are created.")

if __name__ == "__main__":
    import os
    import sys
    # Add backend to path for imports
    sys.path.append(os.getcwd())
    asyncio.run(migrate_interview_table())
