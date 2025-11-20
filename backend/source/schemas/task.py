from pydantic import BaseModel
from datetime import datetime


class TaskGetParams(BaseModel):
    ...


class TaskCreateParams(BaseModel):
    user_id: int
    label_id: int
    
    status_id: int
    priority_id: int
    
    created_at: datetime = datetime.now()
    deadline: datetime
    
    description: str
    executors: list[int]


class TaskResponse(BaseModel):
    owner: str
    status: str
    priority: str
    label: str
    
    created_at: datetime
    deadline: datetime
    
    description: str
    executors: list[str]
    


__all__ = [
    'TaskGetParams',
    'TaskCreateParams',
    'TaskResponse',
]
