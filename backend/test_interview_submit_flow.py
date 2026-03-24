import asyncio
import httpx
import uuid

async def main():
    base_url = "http://127.0.0.1:8001"
    async with httpx.AsyncClient(timeout=60.0) as client:
        # 1. Register
        user_id = str(uuid.uuid4())[:8]
        user_data = {"email": f"test_{user_id}@test.com", "password": "password", "name": "Test User"}
        res = await client.post(f"{base_url}/auth/register", json=user_data)
        token = res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Start Interview
        test_payload = {"topic": "Backend", "difficulty": "easy", "num_questions": 2}
        res = await client.post(f"{base_url}/interviews/start", json=test_payload, headers=headers)
        print("Start Status:", res.status_code)
        if res.status_code != 201:
            print("Start Return:", res.text)
            return
        
        i_data = res.json()
        i_id = i_data["interview_id"]
        print("Started Interview ID:", i_id)
        
        # 3. Submit Answer
        submit_payload = {"answer": "I would use a database indexing strategy."}
        res = await client.post(f"{base_url}/interviews/{i_id}/answer", json=submit_payload, headers=headers)
        print("Submit Status:", res.status_code)
        print("Submit Response:", res.text)

if __name__ == "__main__":
    asyncio.run(main())
