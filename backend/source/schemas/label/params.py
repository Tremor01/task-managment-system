
from pydantic import BaseModel


class GetLabels(BaseModel):
    ...


class CreateLabel(BaseModel):
    name: str

