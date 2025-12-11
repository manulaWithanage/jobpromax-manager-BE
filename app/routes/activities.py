from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from beanie import PydanticObjectId

from app.models.activity import ActivityLog, ActionType
from app.models.user import User, UserRole
from app.auth import get_current_user, require_role

router = APIRouter()


class ActivityResponse(BaseModel):
    id: str
    userId: str
    userName: str
    userRole: str
    action: str
    targetType: Optional[str] = None
    targetId: Optional[str] = None
    targetName: Optional[str] = None
    details: Optional[dict] = None
    timestamp: datetime


def activity_to_response(activity: ActivityLog) -> ActivityResponse:
    """Convert ActivityLog document to response model"""
    return ActivityResponse(
        id=str(activity.id),
        userId=str(activity.userId),
        userName=activity.userName,
        userRole=activity.userRole,
        action=activity.action.value,
        targetType=activity.targetType.value if activity.targetType else None,
        targetId=str(activity.targetId) if activity.targetId else None,
        targetName=activity.targetName,
        details=activity.details,
        timestamp=activity.timestamp
    )


# GET /api/activities - List all activities (Manager only, paginated)
@router.get("/", response_model=List[ActivityResponse])
async def list_activities(
    user_id: Optional[str] = Query(None, alias="userId", description="Filter by user ID"),
    action: Optional[str] = Query(None, description="Filter by action type"),
    limit: int = Query(50, ge=1, le=100, description="Number of results to return"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    current_user: User = Depends(require_role([UserRole.MANAGER]))
):
    """List all activities with optional filters. Manager only."""
    
    query = {}
    
    if user_id:
        try:
            query["userId"] = PydanticObjectId(user_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    if action:
        # Validate action type
        try:
            ActionType(action)
            query["action"] = action
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid action type: {action}")
    
    activities = await ActivityLog.find(query).sort("-timestamp").skip(offset).limit(limit).to_list()
    
    return [activity_to_response(a) for a in activities]


# GET /api/activities/user/:userId - Get activities for specific user (Manager only)
@router.get("/user/{user_id}", response_model=List[ActivityResponse])
async def get_user_activities(
    user_id: str,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(require_role([UserRole.MANAGER]))
):
    """Get activities for a specific user. Manager only."""
    
    try:
        uid = PydanticObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    activities = await ActivityLog.find(
        {"userId": uid}
    ).sort("-timestamp").skip(offset).limit(limit).to_list()
    
    return [activity_to_response(a) for a in activities]


# GET /api/activities/me - Get current user's activities
@router.get("/me", response_model=List[ActivityResponse])
async def get_my_activities(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user)
):
    """Get current user's own activity history."""
    
    activities = await ActivityLog.find(
        {"userId": current_user.id}
    ).sort("-timestamp").skip(offset).limit(limit).to_list()
    
    return [activity_to_response(a) for a in activities]
