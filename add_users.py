
import asyncio
from app.database import init_db
from app.models.user import User, UserRole
from app.utils.security import hash_password

async def add_users():
    print("Connecting to MongoDB...")
    await init_db()
    
    users_to_add = [
        {
            "email": "manager@jobpromax.com",
            "name": "Manager User",
            "password": "manager123",
            "role": UserRole.MANAGER
        },
        {
            "email": "developer@jobpromax.com",
            "name": "Developer User",
            "password": "dev123",
            "role": UserRole.DEVELOPER
        }
    ]

    print("Adding users...")
    for user_data in users_to_add:
        # Check if user exists
        existing_user = await User.find_one(User.email == user_data["email"])
        if existing_user:
            print(f"User {user_data['email']} already exists. Skipping.")
            continue

        new_user = User(
            email=user_data["email"],
            name=user_data["name"],
            password_hash=hash_password(user_data["password"]),
            role=user_data["role"]
        )
        await new_user.insert()
        print(f"Added {user_data['role'].value}: {user_data['email']}")

    print("\nUsers added successfully!")

if __name__ == "__main__":
    asyncio.run(add_users())
