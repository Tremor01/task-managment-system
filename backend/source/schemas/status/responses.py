from pydantic import BaseModel
from datetime import datetime


class Status(BaseModel):
    name: str
    
    
class GetStatuses(BaseModel):
    items: list[Status]

