from beanie import Document
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, List

# KPI Models
class KPI(Document):
    """
    Storing KPIs as a document for simplicity, though often calculated.
    Using a 'type' or 'key' to distinguish if multiple sets exist, 
    or just one single document for global stats.
    """
    label: str
    value: str
    change: Optional[str] = None
    trend: Optional[str] = None # 'up' | 'down' | 'neutral'

    class Settings:
        name = "dashboard_kpis"

# Pipeline Models
class PipelineType(str, Enum):
    INCOMING = 'Incoming'
    WISHLIST = 'Wishlist'

class PipelinePriority(str, Enum):
    HIGH = 'High'
    MEDIUM = 'Medium'
    LOW = 'Low'

class PipelineItem(Document):
    title: str
    type: PipelineType
    priority: Optional[PipelinePriority] = None # For Incoming
    estEffort: Optional[str] = None # For Incoming
    requester: Optional[str] = None # For Wishlist
    dateAdded: Optional[str] = None # For Wishlist

    class Settings:
        name = "pipeline_items"

# Chart Models
class ChartDataPoint(BaseModel):
    name: str # X-axis label (e.g., date or sprint)
    value: Optional[float] = None
    # For burnup:
    totalScope: Optional[float] = None
    completed: Optional[float] = None
    # For velocity:
    velocity: Optional[float] = None

class ChartData(Document):
    chart_type: str # 'burnup' or 'velocity'
    data_points: List[ChartDataPoint]

    class Settings:
        name = "chart_data"
