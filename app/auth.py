from fastapi import Depends, HTTPException, status, Request
from app.utils.security import decode_access_token
from app.models.user import User, UserRole

async def get_current_user(request: Request) -> User:
    """Extract and validate JWT from cookie, return User object."""
    token = request.cookies.get("auth-token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    
    user_id = payload.get("sub")
    user = await User.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    return user

async def verify_token(request: Request) -> dict:
    """Dependency that just returns the token payload (for router-level auth)."""
    token = request.cookies.get("auth-token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    
    return payload

def require_role(allowed_roles: list[UserRole]):
    """Factory for role-based access control."""
    async def role_checker(user: User = Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return user
    return role_checker
