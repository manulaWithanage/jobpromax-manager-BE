from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.config import settings
from app.models.task import Task
from app.models.roadmap import RoadmapPhase
from app.models.feature import Feature
from app.models.dashboard import KPI, PipelineItem, ChartData
from app.models.user import User
from app.models.report import IncidentReport
from app.models.activity import ActivityLog

import certifi

async def init_db():
    client = AsyncIOMotorClient(settings.MONGODB_URI, tlsCAFile=certifi.where())
    database = client[settings.DATABASE_NAME]
    
    await init_beanie(
        database=database,
        document_models=[
            Task,
            RoadmapPhase,
            Feature,
            KPI,
            PipelineItem,
            ChartData,
            User,
            IncidentReport,
            ActivityLog
        ]
    )

