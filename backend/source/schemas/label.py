from pydantic import BaseModel


class LabelGetParams(BaseModel):
    ...


class LabelCreateParams(BaseModel):
    name: str


class LabelResponse(BaseModel):
    name: str


__all__ = [
    'LabelGetParams',
    'LabelCreateParams',
    'LabelResponse',
]
