from pydantic import BaseModel
from datetime import datetime


    
class GetStatuses(BaseModel):
    ...


class CreateStatus(BaseModel):
    name: str
