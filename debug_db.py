
import asyncio
from app.database import init_db
from app.models.task import Task
from app.models.roadmap import RoadmapPhase
from app.models.feature import Feature
from app.models.dashboard import KPI, PipelineItem, ChartData
from app.models.user import User

async def check_db():
    print("Connecting to MongoDB...")
    try:
        await init_db()
        print("Connected successfully!")
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    models = {
        "User": User,
        "Task": Task,
        "RoadmapPhase": RoadmapPhase,
        "Feature": Feature,
        "KPI": KPI,
        "PipelineItem": PipelineItem,
        "ChartData": ChartData
    }

    print("\n--- Database Content Summary ---")
    for name, model in models.items():
        try:
            count = await model.count()
            print(f"{name}: {count} documents")
        except Exception as e:
            print(f"Error querying {name}: {e}")

if __name__ == "__main__":
    asyncio.run(check_db())
