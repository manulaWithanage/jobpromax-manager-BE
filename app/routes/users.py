from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from pydantic import BaseModel, EmailStr
from beanie import PydanticObjectId
from app.auth import get_current_user, require_role
from app.models.user import User, UserRole
from app.models.activity import ActionType, TargetType
from app.utils.security import hash_password
from app.utils.activity_logger import log_activity

router = APIRouter()

class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    role: UserRole
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str

@router.get("/", response_model=List[UserResponse])
async def list_users(current_user: User = Depends(require_role([UserRole.MANAGER]))):
    users = await User.find_all().to_list()
    return [
        UserResponse(
            id=str(u.id),
            name=u.name,
            email=u.email,
            role=u.role.value
        )
        for u in users
    ]

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: CreateUserRequest,
    current_user: User = Depends(require_role([UserRole.MANAGER]))
):
    # Check if email already exists
    existing = await User.find_one(User.email == data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password and create user
    new_user = User(
        email=data.email,
        name=data.name,
        password_hash=hash_password(data.password),
        role=data.role
    )
    await new_user.insert()
    
    # Log USER_CREATED activity
    await log_activity(
        user=current_user,
        action=ActionType.USER_CREATED,
        target_type=TargetType.USER,
        target_id=new_user.id,
        target_name=new_user.name
    )
    
    return UserResponse(
        id=str(new_user.id),
        name=new_user.name,
        email=new_user.email,
        role=new_user.role.value
    )

@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    current_user: User = Depends(require_role([UserRole.MANAGER]))
):
    # Cannot delete self
    if str(current_user.id) == user_id:
        raise HTTPException(status_code=403, detail="Cannot delete yourself")
    
    # Find and delete user
    try:
        user = await User.get(PydanticObjectId(user_id))
    except Exception:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_name = user.name
    await user.delete()
    
    # Log USER_DELETED activity
    await log_activity(
        user=current_user,
        action=ActionType.USER_DELETED,
        target_type=TargetType.USER,
        target_id=PydanticObjectId(user_id),
        target_name=user_name
    )
    
    return {"message": "User deleted successfully", "id": user_id}

