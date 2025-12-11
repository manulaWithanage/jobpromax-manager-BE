from fastapi import APIRouter, HTTPException, Response, Request
from pydantic import BaseModel, EmailStr
from app.models.user import User
from app.models.activity import ActivityLog, ActionType
from app.utils.security import verify_password, create_access_token, decode_access_token

router = APIRouter()

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str

@router.post("/login")
async def login(request: LoginRequest, response: Response):
    # Find user by email
    user = await User.find_one(User.email == request.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create JWT token
    token = create_access_token(data={"sub": str(user.id), "email": user.email, "role": user.role.value})
    
    # Set HTTP-only cookie
    response.set_cookie(
        key="auth-token",
        value=token,
        httponly=True,
        secure=False,  # Set to True in production (HTTPS)
        samesite="lax",
        max_age=60 * 60 * 24 * 7  # 7 days (604800 seconds)
    )
    
    # Log LOGIN activity
    activity = ActivityLog(
        userId=user.id,
        userName=user.name,
        userRole=user.role.value,
        action=ActionType.LOGIN
    )
    await activity.insert()
    
    return {"message": "Login successful", "user": UserResponse(
        id=str(user.id),
        name=user.name,
        email=user.email,
        role=user.role.value
    )}

@router.post("/logout")
async def logout(response: Response, req: Request):
    # Try to get user from token before clearing cookie
    token = req.cookies.get("auth-token")
    if token:
        payload = decode_access_token(token)
        if payload:
            user_id = payload.get("sub")
            user = await User.get(user_id)
            if user:
                # Log LOGOUT activity
                activity = ActivityLog(
                    userId=user.id,
                    userName=user.name,
                    userRole=user.role.value,
                    action=ActionType.LOGOUT
                )
                await activity.insert()
    
    response.delete_cookie(key="auth-token")
    return {"message": "Logged out successfully"}

@router.get("/me", response_model=UserResponse)
async def get_current_user(request: Request):
    token = request.cookies.get("auth-token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_id = payload.get("sub")
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return UserResponse(
        id=str(user.id),
        name=user.name,
        email=user.email,
        role=user.role.value
    )

