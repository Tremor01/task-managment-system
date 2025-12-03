from pydantic import BaseModel


class Status(BaseModel):
    id: int
    name: str
    
    
class GetStatuses(BaseModel):
    items: list[Status]

