from fastapi import APIRouter, HTTPException
from typing import List
from beanie import PydanticObjectId
from app.models.feature import Feature

router = APIRouter()

@router.get("/features", response_model=List[Feature])
async def get_features():
    return await Feature.find_all().to_list()

@router.post("/features", response_model=Feature)
async def create_feature(feature: Feature):
    await feature.insert()
    return feature

@router.patch("/features/{id}", response_model=Feature)
async def update_feature(id: PydanticObjectId, feature_data: Feature):
    feature = await Feature.get(id)
    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")
    
    feature_dict = feature_data.dict(exclude_unset=True, exclude={"id"})
    for key, value in feature_dict.items():
        setattr(feature, key, value)
        
    await feature.save()
    return feature

@router.delete("/features/{id}")
async def delete_feature(id: PydanticObjectId):
    feature = await Feature.get(id)
    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")
    await feature.delete()
    return {"message": "Feature deleted"}
