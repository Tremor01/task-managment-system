from pydantic import BaseModel, Field
from datetime import datetime


class Task(BaseModel):
    task_id: int = Field(validation_alias='id')
    status: str | None = None
    priority: str | None = None
    label: str | None = None
    
    created_at: datetime
    deadline: datetime | None = None
    
    description: str
    
    
class GetTasks(BaseModel):
    items: list[Task]


class CreateTask(BaseModel):
    status: str
