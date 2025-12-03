from pydantic import BaseModel
from datetime import datetime


class Task(BaseModel):
    owner: str
    status: str
    priority: str
    label: str
    
    created_at: datetime
    deadline: datetime
    
    description: str
    executors: list[str]
    
    
class GetTasks(BaseModel):
    items: list[Task]


class CreateTask(BaseModel):
    status: str
