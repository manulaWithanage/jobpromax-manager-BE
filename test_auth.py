import asyncio
import httpx

BASE_URL = "http://127.0.0.1:8000"

async def test_auth_flow():
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
        print("=" * 50)
        print("TEST 1: Login with Manager credentials")
        print("=" * 50)
        
        login_resp = await client.post("/auth/login", json={
            "email": "manager@jobpromax.com",
            "password": "manager123"
        })
        print(f"Status: {login_resp.status_code}")
        print(f"Response: {login_resp.json()}")
        
        # Extract cookie
        cookies = login_resp.cookies
        print(f"Cookies: {dict(cookies)}")
        
        print("\n" + "=" * 50)
        print("TEST 2: Access /auth/me with cookie")
        print("=" * 50)
        
        me_resp = await client.get("/auth/me", cookies=cookies)
        print(f"Status: {me_resp.status_code}")
        print(f"Response: {me_resp.json()}")
        
        print("\n" + "=" * 50)
        print("TEST 3: Access /tasks (protected) with cookie")
        print("=" * 50)
        
        tasks_resp = await client.get("/tasks", cookies=cookies)
        print(f"Status: {tasks_resp.status_code}")
        if tasks_resp.status_code == 200:
            print(f"Tasks count: {len(tasks_resp.json())}")
        else:
            print(f"Response: {tasks_resp.text}")
        
        print("\n" + "=" * 50)
        print("TEST 4: Access /users (Manager only) with cookie")
        print("=" * 50)
        
        users_resp = await client.get("/users/", cookies=cookies)
        print(f"Status: {users_resp.status_code}")
        print(f"Response: {users_resp.json()}")
        
        print("\n" + "=" * 50)
        print("TEST 5: Logout")
        print("=" * 50)
        
        logout_resp = await client.post("/auth/logout", cookies=cookies)
        print(f"Status: {logout_resp.status_code}")
        print(f"Response: {logout_resp.json()}")
        
        print("\n" + "=" * 50)
        print("TEST 6: Access /tasks WITHOUT cookie (should fail)")
        print("=" * 50)
        
        no_auth_resp = await client.get("/tasks")
        print(f"Status: {no_auth_resp.status_code}")
        print(f"Response: {no_auth_resp.json()}")
        
        print("\n" + "=" * 50)
        print("ALL TESTS COMPLETED")
        print("=" * 50)

if __name__ == "__main__":
    asyncio.run(test_auth_flow())
