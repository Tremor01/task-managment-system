from pydantic import BaseModel


class Label(BaseModel):
    id: int
    name: str


class GetLabels(BaseModel):
    items: list[Label]
