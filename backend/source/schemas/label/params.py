
from pydantic import BaseModel


class GetLabels(BaseModel):
    ...


class CreateLabel(BaseModel):
    name: str


class DeleteLabel(BaseModel):
    label_id: int
