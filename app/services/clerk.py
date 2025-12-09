import httpx
from app.config import settings

BASE_URL = "https://api.clerk.com/v1"

async def get_users():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/users",
            headers={"Authorization": f"Bearer {settings.CLERK_SECRET_KEY}"}
        )
        response.raise_for_status()
        return response.json()

async def create_user(data: dict):
    # Map fields to Clerk API expected format if necessary
    # Example: data might have 'name', 'email', 'role'
    # Clerk expects 'email_address', 'first_name', 'last_name', 'public_metadata' etc.
    
    first_name = data.get("name", "").split(" ")[0]
    last_name = " ".join(data.get("name", "").split(" ")[1:]) if " " in data.get("name", "") else ""
    
    payload = {
        "email_address": [data.get("email")],
        "first_name": first_name,
        "last_name": last_name,
        "public_metadata": {"role": data.get("role")},
        "password": data.get("password"),
        "skip_password_checks": True # If we want to allow simple passwords for now
    }
    
    # Remove None or key if password not provided? Clerk might require it or handle invitation.
    # Requirements said "password (optional temporary)"
    if not payload["password"]:
        del payload["password"]
        del payload["skip_password_checks"]

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/users",
            json=payload,
            headers={"Authorization": f"Bearer {settings.CLERK_SECRET_KEY}"}
        )
        response.raise_for_status()
        return response.json()

async def delete_user(user_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{BASE_URL}/users/{user_id}",
            headers={"Authorization": f"Bearer {settings.CLERK_SECRET_KEY}"}
        )
        response.raise_for_status()
        return {"message": "User deleted successfully"}
