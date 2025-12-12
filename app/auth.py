from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from app.utils.security import decode_access_token
from app.models.user import User, UserRole

# OAuth2 scheme for Swagger UI - makes token optional to also support cookies
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


async def get_token_from_request(request: Request, token: Optional[str] = Depends(oauth2_scheme)) -> str:
    """Extract token from Bearer header or cookie."""
    # Priority 1: Bearer token from header (for Swagger)
    if token:
        return token
    
    # Priority 2: Cookie (for browser clients)
    cookie_token = request.cookies.get("auth-token")
    if cookie_token:
        return cookie_token
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user(request: Request, token: Optional[str] = Depends(oauth2_scheme)) -> User:
    """Extract and validate JWT from header or cookie, return User object."""
    auth_token = await get_token_from_request(request, token)
    
    payload = decode_access_token(auth_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    user = await User.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def verify_token(request: Request, token: Optional[str] = Depends(oauth2_scheme)) -> dict:
    """Dependency that just returns the token payload (for router-level auth)."""
    auth_token = await get_token_from_request(request, token)
    
    payload = decode_access_token(auth_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
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
