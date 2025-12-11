from beanie import Document
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
from beanie import PydanticObjectId


class ImpactLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ReportStatus(str, Enum):
    PENDING = "pending"
    ACKNOWLEDGED = "acknowledged"
    ADDRESSED = "addressed"


class Reporter(BaseModel):
    """Nested model for reporter info"""
    id: Optional[PydanticObjectId] = None  # Nullable if public/anonymous
    name: str
    email: Optional[str] = None


class AdminNote(BaseModel):
    """Nested model for admin notes"""
    authorId: PydanticObjectId
    authorName: str
    note: str
    createdAt: datetime = Field(default_factory=datetime.utcnow)


class IncidentReport(Document):
    """Incident Report document for tracking issues"""
    featureId: Optional[PydanticObjectId] = None  # Reference to Features
    reporter: Reporter
    impactLevel: ImpactLevel = ImpactLevel.MEDIUM
    description: str
    status: ReportStatus = ReportStatus.PENDING
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    resolvedAt: Optional[datetime] = None
    adminNotes: List[AdminNote] = []

    class Settings:
        name = "incident_reports"
