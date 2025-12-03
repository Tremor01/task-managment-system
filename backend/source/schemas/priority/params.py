
from pydantic import BaseModel


class GetPriorities(BaseModel):
    ...


class CreatePriority(BaseModel):
    name: str
