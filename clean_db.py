
import asyncio
from app.database import init_db
from app.models.task import Task
from app.models.roadmap import RoadmapPhase
from app.models.feature import Feature
from app.models.dashboard import KPI, PipelineItem, ChartData
from app.models.user import User

async def clean_data():
    print("Connecting to MongoDB...")
    await init_db()
    
    print("Cleaning data...")
    try:
        await Task.delete_all()
        print("- Tasks cleaned")
        
        await RoadmapPhase.delete_all()
        print("- Roadmap cleaned")
        
        await Feature.delete_all()
        print("- Features cleaned")
        
        await KPI.delete_all()
        print("- KPIs cleaned")
        
        await PipelineItem.delete_all()
        print("- Pipeline cleaned")
        
        await ChartData.delete_all()
        print("- Charts cleaned")
        
        await User.delete_all()
        print("- Users cleaned")
        
        print("\nDatabase cleaned successfully!")
    except Exception as e:
        print(f"Error cleaning database: {e}")

if __name__ == "__main__":
    asyncio.run(clean_data())
