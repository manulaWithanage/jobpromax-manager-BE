from fastapi import APIRouter, HTTPException
from typing import List
from beanie import PydanticObjectId
from app.models.task import Task

router = APIRouter()

@router.get("/tasks", response_model=List[Task])
async def get_tasks():
    return await Task.find_all().to_list()

@router.patch("/tasks/{id}", response_model=Task)
async def update_task(id: PydanticObjectId, task_data: Task):
    # Using the whole model for partial updates as per simple requirements,
    # or typically we'd use a separate Pydantic model with optional fields.
    task = await Task.get(id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Simple dictionary update for now, ideally Pydantic's copy(update=...)
    task_dict = task_data.dict(exclude_unset=True, exclude={"id"})
    for key, value in task_dict.items():
        setattr(task, key, value)
    
    await task.save()
    return task
