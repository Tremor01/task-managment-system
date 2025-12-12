from fastapi import APIRouter, Depends, status
from .api_settings import Paths, PREFIX

from ...schemas.priority import params, responses
from ...services import PriorityService, get_priority_service


TAGS = ["Priorities"]
router = APIRouter(prefix=PREFIX, tags=TAGS)  # type: ignore


@router.get(
    path=Paths.GetPriorities,
    name="Get Priority",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": responses.GetPriorities},
        status.HTTP_404_NOT_FOUND: {},
        status.HTTP_400_BAD_REQUEST: {}
    }
)
async def get_priority(
    parameters: params.GetPriorities = Depends(),
    service: PriorityService = Depends(get_priority_service)
):
    return await service.get_priorities(parameters)


@router.post(
    path=Paths.CreatePriority,
    name="Create Priority",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": responses.Priority},
        status.HTTP_404_NOT_FOUND: {},
        status.HTTP_400_BAD_REQUEST: {}
    }
)
async def create_priority(
    parameters: params.CreatePriority,
    service: PriorityService = Depends(get_priority_service)
):
    return await service.create_priority(parameters)


@router.delete(
    path=Paths.DeletePriority,
    name="Delete Priority",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": responses.Priority},
        status.HTTP_404_NOT_FOUND: {},
        status.HTTP_400_BAD_REQUEST: {}
    }
)
async def delete_priority(
    id: int,
    service: PriorityService = Depends(get_priority_service)
):
    return await service.delete_priority(id)
