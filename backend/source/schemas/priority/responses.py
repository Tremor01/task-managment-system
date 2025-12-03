from pydantic import BaseModel


class Priority(BaseModel):
    id: int
    name: str


class GetPriorities(BaseModel):
    items: list[Priority]



class CreatePriority(BaseModel):
    status: str
    