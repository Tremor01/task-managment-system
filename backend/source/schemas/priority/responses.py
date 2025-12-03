from pydantic import BaseModel


class Priority(BaseModel):
    name: str


class GetPriorities(BaseModel):
    items: list[Priority]



class CreatePriority(BaseModel):
    status: str
    