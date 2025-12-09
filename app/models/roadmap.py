from beanie import Document
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class DeliverableStatus(str, Enum):
    DONE = 'done'
    PENDING = 'pending'
    IN_PROGRESS = 'in-progress'

class Deliverable(BaseModel):
    text: str
    status: DeliverableStatus

class PhaseStatus(str, Enum):
    COMPLETED = 'completed'
    CURRENT = 'current'
    UPCOMING = 'upcoming'

class HealthStatus(str, Enum):
    ON_TRACK = 'on-track'
    AT_RISK = 'at-risk'
    DELAYED = 'delayed'

class RoadmapPhase(Document):
    phase: str
    date: str
    title: str
    description: str
    status: PhaseStatus
    health: Optional[HealthStatus] = None
    deliverables: List[Deliverable]

    class Settings:
        name = "roadmap_phases"
