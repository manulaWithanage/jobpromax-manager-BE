import httpx
import asyncio
import os
import sys

# Get token from env or args
TOKEN = os.getenv("TEST_TOKEN")
if len(sys.argv) > 1:
    TOKEN = sys.argv[1]

BASE_URL = "http://127.0.0.1:8000"

async def test_endpoint(client, name, url, expected_status_no_token, expected_status_with_token):
    print(f"--- Testing {name} ({url}) ---")
    headers = {}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
        
    try:
        response = await client.get(f"{BASE_URL}{url}", headers=headers)
        status = response.status_code
        
        expected = expected_status_with_token if TOKEN else expected_status_no_token
        
        # Allow 403 for Users endpoint if token is valid but not manager
        if TOKEN and url == "/users/" and status == 403:
             print(f"✅ {name}: {status} Forbidden (Valid token but insufficient role?) - OK")
             return

        if status == expected:
            print(f"✅ {name}: {status} MATCHED Expected ({expected})")
        else:
            print(f"❌ {name}: {status} FAILED (Expected {expected})")
            
    except Exception as e:
        print(f"❌ {name}: Error {e}")

async def verify():
    print(f"Running tests with TOKEN={'YES' if TOKEN else 'NO'}")
    async with httpx.AsyncClient() as client:
        # 1. Public Endpoint
        await test_endpoint(client, "ROOT", "/", 200, 200)

        # 2. Protected Endpoint (Tasks)
        # Without token: 401. With token: 200.
        await test_endpoint(client, "TASKS", "/tasks", 401, 200)

        # 3. Protected Endpoint (Users)
        # Without token: 401. With token: 200 (if manager) or 403.
        await test_endpoint(client, "USERS", "/users/", 401, 200)

if __name__ == "__main__":
    asyncio.run(verify())
