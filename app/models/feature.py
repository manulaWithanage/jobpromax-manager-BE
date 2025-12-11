from beanie import Document
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, List
from datetime import datetime
from beanie import PydanticObjectId


class FeatureStatusEnum(str, Enum):
    OPERATIONAL = 'operational'
    DEGRADED = 'degraded'
    CRITICAL = 'critical'


class HistoryEntry(BaseModel):
    """Daily status history entry"""
    date: str  # Format: YYYY-MM-DD
    status: str


class LastUpdatedBy(BaseModel):
    """Audit trail for last update"""
    userId: PydanticObjectId
    userName: str
    updatedAt: datetime = Field(default_factory=datetime.utcnow)


class Feature(Document):
    name: str
    status: FeatureStatusEnum
    publicNote: str
    linkedTicket: Optional[str] = None
    history: List[HistoryEntry] = []  # 30-60 day history
    lastUpdatedBy: Optional[LastUpdatedBy] = None

    class Settings:
        name = "features"

