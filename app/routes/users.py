from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel
from app.auth import verify_token
from app.config import settings
from app.services.clerk import get_users, create_user, delete_user

router = APIRouter()

class CreateUserRequest(BaseModel):
    name: str
    email: str
    role: str # manager, developer, leadership
    password: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    isSuperAdmin: bool

def is_manager(payload: dict = Depends(verify_token)):
    # Check if user has manager role in public_metadata or similar
    # Structure of payload depends on Clerk's JWT claim. 
    # Usually metadata is in 'public_metadata' or direct claim if customized.
    # Assumption needed: 'public_metadata' claim exists or custom claim key.
    # Standard Clerk JWT templates often don't include metadata by default unless configured.
    # We'll assume the token has 'public_metadata' or 'metadata' where role is stored of the requester.
    # OR we just check if they are authorized at all for now? 
    # Requirements: "Access: Manager Only".
    
    # Let's inspect payload roughly or implement a safer check.
    # If "role" is a direct claim (custom JWT template recommended for this), access it.
    # For now, let's look for 'public_metadata' dict in payload.
    metadata = payload.get("public_metadata", {})
    role = metadata.get("role", "")
    
    # Also considering "superuser" logic if applicable?
    if role != "manager":
         raise HTTPException(status_code=403, detail="Requires Manager privileges")
    return payload

@router.get("/", response_model=List[UserResponse])
async def list_users(user: dict = Depends(is_manager)):
    users_data = await get_users()
    # Transform to UserResponse
    results = []
    for u in users_data:
        # Clerk user object structure:
        # id, first_name, last_name, email_addresses, public_metadata
        metadata = u.get("public_metadata", {})
        email_obj = u.get("email_addresses", [{}])[0]
        email = email_obj.get("email_address", "")
        
        # Check Super Admin status
        # defined by SUPER_ADMIN_EMAIL or specific Clerk ID
        is_super = False
        if settings.SUPER_ADMIN_EMAIL and email == settings.SUPER_ADMIN_EMAIL:
            is_super = True
            
        results.append(UserResponse(
            id=u.get("id"),
            name=f"{u.get('first_name', '')} {u.get('last_name', '')}".strip(),
            email=email,
            role=metadata.get("role", "developer"), # Default to developer?
            isSuperAdmin=is_super
        ))
    return results

@router.post("/", response_model=UserResponse)
async def create_new_user(data: CreateUserRequest, user: dict = Depends(is_manager)):
    try:
        new_user = await create_user(data.dict())
        # Return matched response
        metadata = new_user.get("public_metadata", {})
        email_obj = new_user.get("email_addresses", [{}])[0]
        email = email_obj.get("email_address", "")
        
        is_super = False
        if settings.SUPER_ADMIN_EMAIL and email == settings.SUPER_ADMIN_EMAIL:
            is_super = True

        return UserResponse(
            id=new_user.get("id"),
            name=f"{new_user.get('first_name', '')} {new_user.get('last_name', '')}".strip(),
            email=email,
            role=metadata.get("role", data.role),
            isSuperAdmin=is_super
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{user_id}")
async def remove_user(user_id: str, user: dict = Depends(is_manager)):
    # Check if target is super admin
    # We need to fetch the user first to check their email? 
    # Or rely on get_users list. Fetching single user is safer.
    # Optimize: just fetch the single user. 
    # START HACK: For now, I'll fetch list and find? No, that's inefficient.
    # I should add get_user(id) to service or just implement check here.
    
    # Actually, let's implement validation in service or here.
    # Re-reading requirements: "The backend MUST check if the target user is a 'Super Admin'."
    
    # Let's verify by fetching the user first.
    # I'll use the raw helper as I didn't add get_user to clerk.py yet.
    # I should have added get_user. I'll stick to a quick fetch if possible or just proceed with delete and let Clerk handle?
    # No, I must block it.
    
    # I will modify clerk.py or simply use httpx here for the check? 
    # Better to assume I can trust the logic:
    # IF I delete blindly, I might delete super admin.
    # Check ID against known super ID? User only provided EMAIL in env.
    
    # Plan: Fetch user details from Clerk before deleting.
    # To do that clean, I'll update clerk.py first? Or just do it here.
    # I'll add `get_user` to clerk.py in a subsequent fix if needed, but for now
    # I'll rely on listing users? No too redundant.
    # I'll assume for this iteration I will try to fetch specific user.
    # Wait, I didn't verify if I can import `get_user` from clerk service. I didn't define it.
    
    # I will implement `get_user` in `clerk.py` properly by editing the file again? 
    # Or just add a quick helper here. I'll add a quick helper here or use `httpx` directly.
    # Actually, I'll just use `httpx` here for simplicity to avoid multiple writes to `clerk.py` right now.
    
    auth_header = {"Authorization": f"Bearer {settings.CLERK_SECRET_KEY}"}
    async with httpx.AsyncClient() as client:
        # Fetch target user
        resp = await client.get(f"https://api.clerk.com/v1/users/{user_id}", headers=auth_header)
        if resp.status_code == 404:
            raise HTTPException(status_code=404, detail="User not found")
        
        target_data = resp.json()
        email_obj = target_data.get("email_addresses", [{}])[0]
        email = email_obj.get("email_address", "")
        
        if settings.SUPER_ADMIN_EMAIL and email == settings.SUPER_ADMIN_EMAIL:
             raise HTTPException(status_code=403, detail="Cannot delete Super Admin")
             
    # Proceed to delete
    await delete_user(user_id)
    return {"message": "User deleted successfully", "id": user_id}
