from pydantic import BaseModel


class PriorityGetParams(BaseModel):
    ...


class PriorityCreateParams(BaseModel):
    name: str


class PriorityResponse(BaseModel):
    name: str


__all__ = [
    'PriorityGetParams',
    'PriorityCreateParams',
    'PriorityResponse',
]
