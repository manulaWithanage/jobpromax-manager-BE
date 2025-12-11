from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
from beanie import PydanticObjectId
from datetime import datetime, date

from app.models.feature import Feature, FeatureStatusEnum, HistoryEntry, LastUpdatedBy
from app.models.activity import ActionType, TargetType
from app.models.user import User
from app.auth import get_current_user
from app.utils.activity_logger import log_activity

router = APIRouter()


class UpdateFeatureRequest(BaseModel):
    """Request model for updating a feature"""
    status: Optional[FeatureStatusEnum] = None
    publicNote: Optional[str] = None
    linkedTicket: Optional[str] = None


@router.get("/features", response_model=List[Feature])
async def get_features():
    return await Feature.find_all().to_list()


@router.post("/features", response_model=Feature)
async def create_feature(feature: Feature):
    await feature.insert()
    return feature


@router.patch("/features/{id}", response_model=Feature)
async def update_feature(
    id: PydanticObjectId, 
    feature_data: UpdateFeatureRequest,
    current_user: User = Depends(get_current_user)
):
    feature = await Feature.get(id)
    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")
    
    old_status = feature.status
    
    # Update fields if provided
    if feature_data.status is not None:
        feature.status = feature_data.status
    if feature_data.publicNote is not None:
        feature.publicNote = feature_data.publicNote
    if feature_data.linkedTicket is not None:
        feature.linkedTicket = feature_data.linkedTicket
    
    # Update lastUpdatedBy
    feature.lastUpdatedBy = LastUpdatedBy(
        userId=current_user.id,
        userName=current_user.name,
        updatedAt=datetime.utcnow()
    )
    
    # Upsert today's history entry (if status changed)
    if feature_data.status is not None:
        today_str = date.today().isoformat()  # YYYY-MM-DD
        
        # Check if today's entry exists
        existing_entry_idx = None
        for i, entry in enumerate(feature.history):
            if entry.date == today_str:
                existing_entry_idx = i
                break
        
        if existing_entry_idx is not None:
            # Update existing entry
            feature.history[existing_entry_idx].status = feature.status.value
        else:
            # Add new entry
            feature.history.append(HistoryEntry(
                date=today_str,
                status=feature.status.value
            ))
        
        # Retain max 60 entries (trim oldest if needed)
        if len(feature.history) > 60:
            feature.history = feature.history[-60:]
    
    await feature.save()
    
    # Log activity if status changed
    if feature_data.status is not None and old_status != feature.status:
        await log_activity(
            user=current_user,
            action=ActionType.FEATURE_STATUS_UPDATE,
            target_type=TargetType.FEATURE,
            target_id=feature.id,
            target_name=feature.name,
            details={"oldStatus": old_status.value, "newStatus": feature.status.value}
        )
    
    return feature


@router.delete("/features/{id}")
async def delete_feature(id: PydanticObjectId):
    feature = await Feature.get(id)
    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")
    await feature.delete()
    return {"message": "Feature deleted"}

