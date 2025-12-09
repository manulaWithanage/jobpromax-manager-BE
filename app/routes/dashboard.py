from fastapi import APIRouter, HTTPException
from typing import List
from beanie import PydanticObjectId
from app.models.dashboard import KPI, PipelineItem, ChartData, ChartDataPoint

router = APIRouter()

@router.get("/dashboard/kpi", response_model=List[KPI])
async def get_kpis():
    return await KPI.find_all().to_list()

@router.get("/pipeline", response_model=List[PipelineItem])
async def get_pipeline():
    return await PipelineItem.find_all().to_list()

@router.post("/pipeline", response_model=PipelineItem)
async def create_pipeline_item(item: PipelineItem):
    await item.insert()
    return item

@router.patch("/pipeline/{id}", response_model=PipelineItem)
async def update_pipeline_item(id: PydanticObjectId, item_data: PipelineItem):
    item = await PipelineItem.get(id)
    if not item:
        raise HTTPException(status_code=404, detail="Pipeline Item not found")
        
    item_dict = item_data.dict(exclude_unset=True, exclude={"id"})
    for key, value in item_dict.items():
        setattr(item, key, value)
        
    await item.save()
    return item

@router.delete("/pipeline/{id}")
async def delete_pipeline_item(id: PydanticObjectId):
    item = await PipelineItem.get(id)
    if not item:
        raise HTTPException(status_code=404, detail="Pipeline Item not found")
    await item.delete()
    return {"message": "Pipeline Item deleted"}

@router.get("/dashboard/charts/burnup", response_model=List[ChartDataPoint])
async def get_burnup_chart():
    chart = await ChartData.find_one(ChartData.chart_type == "burnup")
    if chart:
        return chart.data_points
    return []

@router.get("/dashboard/charts/velocity", response_model=List[ChartDataPoint])
async def get_velocity_chart():
    chart = await ChartData.find_one(ChartData.chart_type == "velocity")
    if chart:
        return chart.data_points
    return []
