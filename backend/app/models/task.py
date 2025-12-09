from beanie import Document
from pydantic import Field
from enum import Enum
from typing import Optional
from datetime import datetime

class TaskStatus(str, Enum):
    IN_PROGRESS = 'In Progress'
    IN_REVIEW = 'In Review'
    BLOCKED = 'Blocked'
    DONE = 'Done'

class TaskPriority(str, Enum):
    HIGH = 'High'
    MEDIUM = 'Medium'
    LOW = 'Low'

class Task(Document):
    name: str
    assignee: str
    status: TaskStatus
    dueDate: str  # Keeping as string to match simple requirements, can be datetime
    priority: Optional[TaskPriority] = None

    class Settings:
        name = "tasks"
