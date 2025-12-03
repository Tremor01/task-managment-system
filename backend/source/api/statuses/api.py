from fastapi import APIRouter, Depends, status
from .api_settings import Paths, PREFIX

from schemas.status import params, responses
from services import StatusService, get_status_service


TAGS = ["Statuses"]
router = APIRouter(prefix=PREFIX, tags=TAGS)  # type: ignore


@router.get(
    path=Paths.GetStatuses,
    name="Get Status",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": responses.GetStatuses},
        status.HTTP_404_NOT_FOUND: {},
        status.HTTP_400_BAD_REQUEST: {}
    }
)
async def get_status(
    parameters: params.GetStatuses = Depends(),
    service: StatusService = Depends(get_status_service)
):
    return await service.get_statuses(parameters)


@router.post(
    path=Paths.CreateStatus,
    name="Create Status",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": responses.Status},
        status.HTTP_404_NOT_FOUND: {},
        status.HTTP_400_BAD_REQUEST: {}
    }
)
async def create_status(
    parameters: params.CreateStatus,
    service: StatusService = Depends(get_status_service)
):
    return await service.create_status(parameters)



@router.delete(
    path=Paths.DeleteStatus,
    name="Delete Status",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": responses.Status},
        status.HTTP_404_NOT_FOUND: {},
        status.HTTP_400_BAD_REQUEST: {}
    }
)
async def delete_status(
    id: int,
    service: StatusService = Depends(get_status_service)
):
    return await service.delete_status(id)

