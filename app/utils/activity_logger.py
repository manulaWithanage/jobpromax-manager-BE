from app.models.activity import ActivityLog, ActionType, TargetType
from app.models.user import User
from typing import Optional, Dict, Any
from beanie import PydanticObjectId


async def log_activity(
    user: User,
    action: ActionType,
    target_type: Optional[TargetType] = None,
    target_id: Optional[PydanticObjectId] = None,
    target_name: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
) -> ActivityLog:
    """
    Log a user activity to the database.
    
    Args:
        user: The user performing the action
        action: The type of action (from ActionType enum)
        target_type: The type of entity being acted upon
        target_id: The ID of the target entity
        target_name: Human-readable name of the target
        details: Additional context about the action
    
    Returns:
        The created ActivityLog document
    """
    activity = ActivityLog(
        userId=user.id,
        userName=user.name,
        userRole=user.role.value,
        action=action,
        targetType=target_type,
        targetId=target_id,
        targetName=target_name,
        details=details
    )
    await activity.insert()
    return activity
