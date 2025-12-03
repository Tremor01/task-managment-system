from pydantic import BaseModel
from datetime import datetime


class GetTasks(BaseModel):
    ...


class CreateTask(BaseModel):
    label_id: int | None = None
    status_id: int | None = None
    priority_id: int | None = None
    
    created_at: datetime = datetime.now() 
    deadline: datetime | None = None
    
    description: str
    executors: list[int] | None = None


class UpdateTask(BaseModel):
    task_id: int
    
    label_id: int | None = None
    status_id: int | None = None
    priority_id: int | None = None
    deadline: datetime | None = None
    
    description: str | None = None
    executors: list[int] | None = None

    