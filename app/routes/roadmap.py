from fastapi import APIRouter, HTTPException, Depends
from typing import List
from beanie import PydanticObjectId

from app.models.roadmap import RoadmapPhase
from app.models.activity import ActionType, TargetType
from app.models.user import User
from app.auth import get_current_user
from app.utils.activity_logger import log_activity

router = APIRouter()

@router.get("/roadmap", response_model=List[RoadmapPhase])
async def get_roadmap():
    return await RoadmapPhase.find_all().to_list()

@router.post("/roadmap", response_model=RoadmapPhase)
async def create_roadmap_phase(phase: RoadmapPhase):
    await phase.insert()
    return phase

@router.patch("/roadmap/{id}", response_model=RoadmapPhase)
async def update_roadmap_phase(
    id: PydanticObjectId, 
    phase_data: RoadmapPhase,
    current_user: User = Depends(get_current_user)
):
    phase = await RoadmapPhase.get(id)
    if not phase:
        raise HTTPException(status_code=404, detail="Roadmap Phase not found")
    
    phase_dict = phase_data.dict(exclude_unset=True, exclude={"id"})
    for key, value in phase_dict.items():
        setattr(phase, key, value)
        
    await phase.save()
    
    # Log ROADMAP_PHASE_UPDATE activity
    await log_activity(
        user=current_user,
        action=ActionType.ROADMAP_PHASE_UPDATE,
        target_type=TargetType.ROADMAP,
        target_id=phase.id,
        target_name=phase.title
    )
    
    return phase

@router.delete("/roadmap/{id}")
async def delete_roadmap_phase(id: PydanticObjectId):
    phase = await RoadmapPhase.get(id)
    if not phase:
        raise HTTPException(status_code=404, detail="Roadmap Phase not found")
    await phase.delete()
    return {"message": "Roadmap Phase deleted"}

