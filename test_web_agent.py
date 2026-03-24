import asyncio
import os
import sys

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from backend.ai.agents.web_agent import web_agent

async def main():
    print("Testing get_company_requirements for Google UI Designer...")
    skills = await web_agent.get_company_requirements("Google", "UI Designer")
    print("----- RESULT -----")
    print(skills)

if __name__ == "__main__":
    asyncio.run(main())
