import asyncio
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from config import settings
from sqlalchemy.ext.asyncio import create_async_engine

async def test_db():
    print(f"Testing connection to: {settings.DATABASE_URL}")
    try:
        engine = create_async_engine(settings.DATABASE_URL)
        async with engine.connect() as conn:
            print("Successfully connected to the database!")
            await conn.close()
    except Exception as e:
        print(f"Database connection FAILED: {e}")

async def test_rag():
    try:
        from ai.rag_pipeline import rag_pipeline
        print("Initializing RAG pipeline...")
        await rag_pipeline.initialize()
        print("RAG pipeline initialized successfully!")
    except Exception as e:
        print(f"RAG initialization FAILED: {e}")

async def main():
    await test_db()
    # await test_rag()

if __name__ == "__main__":
    asyncio.run(main())
