
from pydantic import BaseModel


class GetPriorities(BaseModel):
    ...


class CreatePriority(BaseModel):
    name: str


class DeletePriority(BaseModel):
    priority_id: int