from beanie import Document
from pydantic import Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum
from beanie import PydanticObjectId


class ActionType(str, Enum):
    """All possible activity action types"""
    FEATURE_STATUS_UPDATE = "FEATURE_STATUS_UPDATE"
    REPORT_CREATED = "REPORT_CREATED"
    REPORT_ACKNOWLEDGED = "REPORT_ACKNOWLEDGED"
    REPORT_ADDRESSED = "REPORT_ADDRESSED"
    REPORT_NOTE_ADDED = "REPORT_NOTE_ADDED"
    REPORT_DELETED = "REPORT_DELETED"
    ROADMAP_PHASE_UPDATE = "ROADMAP_PHASE_UPDATE"
    ROADMAP_DELIVERABLE_TOGGLE = "ROADMAP_DELIVERABLE_TOGGLE"
    USER_CREATED = "USER_CREATED"
    USER_DELETED = "USER_DELETED"
    TASK_STATUS_UPDATE = "TASK_STATUS_UPDATE"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"


class TargetType(str, Enum):
    """Target entity types"""
    FEATURE = "feature"
    REPORT = "report"
    ROADMAP = "roadmap"
    USER = "user"
    TASK = "task"


class ActivityLog(Document):
    """Activity log for tracking all user actions"""
    userId: PydanticObjectId
    userName: str
    userRole: str  # 'manager', 'developer', 'leadership'
    action: ActionType
    targetType: Optional[TargetType] = None
    targetId: Optional[PydanticObjectId] = None
    targetName: Optional[str] = None  # Human-readable name
    details: Optional[Dict[str, Any]] = None  # Additional context
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "activity_logs"
