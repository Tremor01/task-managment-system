from fastapi import APIRouter, Depends, status
from .api_settings import Paths, PREFIX

from schemas.priority import *
from services import PriorityService, get_priority_service


TAGS = ["Priorities"]
router = APIRouter(prefix=PREFIX, tags=TAGS)  # type: ignore


@router.get(
    path=Paths.GetPriority,
    name="Get Priority",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": PriorityResponse},
        status.HTTP_404_NOT_FOUND: {},
        status.HTTP_400_BAD_REQUEST: {}
    }
)
async def get_priority(
    parameters: PriorityGetParams = Depends(),
    service: PriorityService = Depends(get_priority_service)
):
    return await service.get_tasks(parameters)


@router.post(
    path=Paths.CreatePriority,
    name="Create Priority",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": PriorityResponse},
        status.HTTP_404_NOT_FOUND: {},
        status.HTTP_400_BAD_REQUEST: {}
    }
)
async def create_priority(
    parameters: PriorityCreateParams = Depends(),
    service: PriorityService = Depends(get_priority_service)
):
    return await service.create_priority(parameters)

