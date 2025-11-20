from pydantic import BaseModel


class StatusGetParams(BaseModel):
    ...


class StatusCreateParams(BaseModel):
    name: str


class StatusResponse(BaseModel):
    name: str


__all__ = [
    'StatusGetParams',
    'StatusCreateParams',
    'StatusResponse',
]
