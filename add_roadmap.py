
import asyncio
from app.database import init_db
from app.models.roadmap import RoadmapPhase, Deliverable, PhaseStatus, HealthStatus, DeliverableStatus

async def add_roadmap():
    print("Connecting to MongoDB...")
    await init_db()
    
    # Sample Data based on a typical software delivery timeline
    roadmap_data = [
        RoadmapPhase(
            phase="Phase 1",
            date="Q1 2024",
            title="Foundation & MVP",
            description="Establishing the core infrastructure, basic user authentication, and initial database schema. Goal is to have a walkable skeleton.",
            status=PhaseStatus.COMPLETED,
            health=HealthStatus.ON_TRACK,
            deliverables=[
                Deliverable(text="Project Setup & Repo Init", status=DeliverableStatus.DONE),
                Deliverable(text="Database Schema Design", status=DeliverableStatus.DONE),
                Deliverable(text="User Authentication API", status=DeliverableStatus.DONE),
                Deliverable(text="Basic Frontend Shell", status=DeliverableStatus.DONE)
            ]
        ),
        RoadmapPhase(
            phase="Phase 2",
            date="Q2 2024",
            title="Core Features Alpha",
            description="Implementation of the primary business logic. Users can perform main tasks. UI is functional but unpolished.",
            status=PhaseStatus.COMPLETED,
            health=HealthStatus.ON_TRACK,
            deliverables=[
                Deliverable(text="Task Management Module", status=DeliverableStatus.DONE),
                Deliverable(text="User Roles & Permissions", status=DeliverableStatus.DONE),
                Deliverable(text="Basic Reporting Dashboard", status=DeliverableStatus.DONE),
                Deliverable(text="Email Notifications", status=DeliverableStatus.DONE)
            ]
        ),
        RoadmapPhase(
            phase="Phase 3",
            date="Q3 2024",
            title="Beta & Polish",
            description="Focus on user experience, performance optimization, and fixing bugs found during Alpha testing. Introducing advanced analytics.",
            status=PhaseStatus.CURRENT,
            health=HealthStatus.ON_TRACK,
            deliverables=[
                Deliverable(text="Advanced Analytics Engine", status=DeliverableStatus.IN_PROGRESS),
                Deliverable(text="UI/UX Visual Overhaul", status=DeliverableStatus.IN_PROGRESS),
                Deliverable(text="Performance Optimization", status=DeliverableStatus.PENDING),
                Deliverable(text="Mobile Responsiveness Fixes", status=DeliverableStatus.PENDING)
            ]
        ),
        RoadmapPhase(
            phase="Phase 4",
            date="Q4 2024",
            title="Scale & Integrations",
            description="Preparing for public launch. Adding third-party integrations (Slack, Jira) and ensuring system can handle high load.",
            status=PhaseStatus.UPCOMING,
            health=HealthStatus.ON_TRACK,
            deliverables=[
                Deliverable(text="Slack Integration", status=DeliverableStatus.PENDING),
                Deliverable(text="Jira Integration", status=DeliverableStatus.PENDING),
                Deliverable(text="Load Balancing Setup", status=DeliverableStatus.PENDING),
                Deliverable(text="Public API Documentation", status=DeliverableStatus.PENDING)
            ]
        )
    ]

    print(f"Adding {len(roadmap_data)} roadmap phases...")
    for phase in roadmap_data:
        await phase.insert()
        print(f"Added phase: {phase.title}")

    print("\nRoadmap data added successfully!")

if __name__ == "__main__":
    asyncio.run(add_roadmap())
