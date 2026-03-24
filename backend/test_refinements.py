
import asyncio
import uuid
import httpx
from datetime import datetime

async def test_refinements():
    base_url = "http://127.0.0.1:8000"
    
    # 1. Register/Login to get token
    u_id = str(uuid.uuid4())[:8]
    test_email = f"test_{u_id}@test.com"
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            # 1. Register/Login to get token
            reg_res = await client.post(f"{base_url}/auth/register", json={
                "email": test_email,
                "password": "password123",
                "name": "Refinement Tester"
            })
            print(f"Registration: {reg_res.status_code}")
            if reg_res.status_code != 201:
                print(f"Registration Error: {reg_res.text}")
                return

            reg_data = reg_res.json()
            if "access_token" in reg_data:
                token = reg_data["access_token"]
            else:
                log_res = await client.post(f"{base_url}/auth/login", json={
                    "email": test_email,
                    "password": "password123"
                })
                if log_res.status_code != 200:
                    print(f"Login Error: {log_res.text}")
                    return
                token = log_res.json().get("access_token")
            
            if not token:
                print("Failed to retrieve access token.")
                return

            headers = {"Authorization": f"Bearer {token}"}

            # 2. Test Skill Gap Persistence
            print("\nTesting Skill Gap Persistence...")
            gap_res = await client.post(f"{base_url}/roadmaps/skill-gap", json={
                "company": "Google",
                "role": "Software Engineer",
                "user_skills": ["Python", "JavaScript"]
            }, headers=headers)
            print(f"Skill Gap Status: {gap_res.status_code}")
            if gap_res.status_code == 200:
                print("Skill Gap Response successfully received.")
            
            # 3. Test Roadmap Generation
            print("\nTesting Roadmap Generation...")
            road_res = await client.post(f"{base_url}/roadmaps/generate", json={
                "company": "Google",
                "role": "Software Engineer",
                "weeks": 4
            }, headers=headers)
            print(f"Roadmap Status: {road_res.status_code}")
            if road_res.status_code == 201:
                plan = road_res.json().get("weekly_plan", [])
                print(f"Roadmap generated with {len(plan)} weeks.")

            # 4. Test Interview
            print("\nTesting Interview Context Awareness...")
            int_res = await client.post(f"{base_url}/interviews/start", json={
                "topic": "System Design",
                "difficulty": "medium",
                "num_questions": 2,
                "company": "Google",
                "role": "Software Engineer"
            }, headers=headers)
            print(f"Interview Start: {int_res.status_code}")
            if int_res.status_code == 201:
                interview_id = int_res.json()["interview_id"]
                ans_res = await client.post(f"{base_url}/interviews/{interview_id}/answer", json={
                    "answer": "I would use a load balancer and multiple microservices."
                }, headers=headers)
                print(f"Answer Submission: {ans_res.status_code}")
    except httpx.RequestError as e:
        print(f"An error occurred while requesting {e.request.url!r}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(test_refinements())
