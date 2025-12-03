from pydantic import BaseModel


class Label(BaseModel):
    name: str


class GetLabels(BaseModel):
    items: list[Label]



class CreateLabel(BaseModel):
    status: str
    