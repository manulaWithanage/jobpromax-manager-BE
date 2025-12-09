import asyncio
from app.database import init_db
from app.models.task import Task, TaskStatus, TaskPriority
from app.models.roadmap import RoadmapPhase, Deliverable, DeliverableStatus, PhaseStatus, HealthStatus
from app.models.feature import Feature, FeatureStatusEnum
from app.models.dashboard import KPI, PipelineItem, PipelineType, PipelinePriority, ChartData, ChartDataPoint

async def seed_data():
    await init_db()
    
    # Clear existing data
    await Task.delete_all()
    await RoadmapPhase.delete_all()
    await Feature.delete_all()
    await KPI.delete_all()
    await PipelineItem.delete_all()
    await ChartData.delete_all()

    # Tasks
    tasks = [
        Task(name="Fix login bug", assignee="John Doe", status=TaskStatus.IN_PROGRESS, dueDate="2024-08-15", priority=TaskPriority.HIGH),
        Task(name="Update documentation", assignee="Jane Smith", status=TaskStatus.DONE, dueDate="2024-08-10", priority=TaskPriority.LOW),
        Task(name="Refactor API", assignee="Bob Johnson", status=TaskStatus.IN_REVIEW, dueDate="2024-08-20", priority=TaskPriority.MEDIUM),
    ]
    for task in tasks:
        await task.insert()
    print("Tasks seeded.")

    # Roadmap
    roadmap = [
        RoadmapPhase(
            phase="Phase 1", date="Q3 2024", title="MVP Launch", description="Initial release of the platform.", 
            status=PhaseStatus.COMPLETED, health=HealthStatus.ON_TRACK,
            deliverables=[
                Deliverable(text="User Authentication", status=DeliverableStatus.DONE),
                Deliverable(text="Basic Dashboard", status=DeliverableStatus.DONE)
            ]
        ),
        RoadmapPhase(
            phase="Phase 2", date="Q4 2024", title="Advanced Features", description="Adding reporting and analytics.", 
            status=PhaseStatus.CURRENT, health=HealthStatus.ON_TRACK,
            deliverables=[
                Deliverable(text="Reporting Module", status=DeliverableStatus.IN_PROGRESS),
                Deliverable(text="Data Export", status=DeliverableStatus.PENDING)
            ]
        )
    ]
    for phase in roadmap:
        await phase.insert()
    print("Roadmap seeded.")

    # Features
    features = [
        Feature(name="User Auth", status=FeatureStatusEnum.OPERATIONAL, publicNote="All systems normal."),
        Feature(name="Reporting", status=FeatureStatusEnum.DEGRADED, publicNote="Experiencing latency."),
        Feature(name="Notifications", status=FeatureStatusEnum.CRITICAL, publicNote="Service down.")
    ]
    for feature in features:
        await feature.insert()
    print("Features seeded.")

    # Dashboard - KPIs
    kpis = [
        KPI(label="Overall Completion", value="68%", change="+5%", trend="up"),
        KPI(label="Current Sprint", value="12/20 Tasks", change="", trend="neutral"),
        KPI(label="Velocity", value="45 pts", change="+2 pts", trend="up")
    ]
    for kpi in kpis:
        await kpi.insert()
    print("KPIs seeded.")

    # Dashboard - Pipeline
    pipeline = [
        PipelineItem(title="Dark Mode Support", type=PipelineType.WISHLIST, requester="User A", dateAdded="2024-08-01"),
        PipelineItem(title="Integration with Slack", type=PipelineType.INCOMING, priority=PipelinePriority.HIGH, estEffort="3 Days")
    ]
    for item in pipeline:
        await item.insert()
    print("Pipeline seeded.")
    
    # Dashboard - Charts
    # Burnup
    burnup_data = [
        ChartDataPoint(name="Week 1", totalScope=50, completed=10),
        ChartDataPoint(name="Week 2", totalScope=50, completed=25),
        ChartDataPoint(name="Week 3", totalScope=55, completed=40)
    ]
    await ChartData(chart_type="burnup", data_points=burnup_data).insert()

    # Velocity
    velocity_data = [
        ChartDataPoint(name="Sprint 1", velocity=30),
        ChartDataPoint(name="Sprint 2", velocity=45),
        ChartDataPoint(name="Sprint 3", velocity=40)
    ]
    await ChartData(chart_type="velocity", data_points=velocity_data).insert()
    print("Charts seeded.")

if __name__ == "__main__":
    asyncio.run(seed_data())
