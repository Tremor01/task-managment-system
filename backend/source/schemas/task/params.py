from pydantic import BaseModel
from datetime import datetime


class GetTasks(BaseModel):
    label: str | None = None
    status: str | None = None
    priority: str | None = None


class CreateTask(BaseModel):
    label_id: int | None = None
    status_id: int | None = None
    priority_id: int | None = None
    
    created_at: datetime = datetime.now() 
    deadline: datetime | None = None
    
    description: str


class UpdateTask(BaseModel):
    task_id: int
    
    label_id: int | None = None
    status_id: int | None = None
    priority_id: int | None = None
    deadline: datetime | None = None
    
    description: str | None = None


class DeleteTask(BaseModel):
    task_id: int
