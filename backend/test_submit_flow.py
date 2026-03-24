import asyncio
import httpx
import uuid

async def main():
    base_url = "http://127.0.0.1:8001"
    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. Register to get token
        user_id = str(uuid.uuid4())[:8]
        user_data = {"email": f"test_{user_id}@test.com", "password": "password", "name": "Test User"}
        print("Registering...")
        res = await client.post(f"{base_url}/auth/register", json=user_data)
        print("Register Status:", res.status_code)
        
        token = res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 3. Generate Test
        test_payload = {"topic": "Python", "num_questions": 2}
        print("Generating test...")
        res = await client.post(f"{base_url}/tests/generate", json=test_payload, headers=headers)
        print("Generate Status:", res.status_code)
        if res.status_code != 201:
            print("Generate Return:", res.text)
            return
        
        test_data = res.json()
        test_id = test_data["test_id"]
        print("Generated Test ID:", test_id)
        
        # 4. Submit Test
        print("Submitting test...")
        submit_payload = {"test_id": test_id, "answers": [0, 1]}
        res = await client.post(f"{base_url}/tests/submit", json=submit_payload, headers=headers)
        print("Submit Status:", res.status_code)
        print("Submit Response:", res.text)

if __name__ == "__main__":
    asyncio.run(main())
