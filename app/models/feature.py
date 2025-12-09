from beanie import Document
from enum import Enum
from typing import Optional

class FeatureStatusEnum(str, Enum):
    OPERATIONAL = 'operational'
    DEGRADED = 'degraded'
    CRITICAL = 'critical'

class Feature(Document):
    name: str
    status: FeatureStatusEnum
    publicNote: str
    linkedTicket: Optional[str] = None

    class Settings:
        name = "features"
