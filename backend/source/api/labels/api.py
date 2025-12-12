from typing import Annotated
from fastapi import APIRouter, Depends, status
from .api_settings import Paths, PREFIX

from ...schemas.label import params, responses
from ...services import LabelService, get_label_service


TAGS = ["Labels"]
router = APIRouter(prefix=PREFIX, tags=TAGS)  # type: ignore


@router.get(
    path=Paths.GetLabel,
    name="Get Label",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": responses.GetLabels},
        status.HTTP_404_NOT_FOUND: {},
        status.HTTP_400_BAD_REQUEST: {}
    }
)
async def get_labels(
    parameters: params.GetLabels = Depends(),
    service: LabelService = Depends(get_label_service)
):
    return await service.get_labels(parameters)


@router.post(
    path=Paths.CreateLabel,
    name="Create Label",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": responses.Label},
        status.HTTP_404_NOT_FOUND: {},
        status.HTTP_400_BAD_REQUEST: {}
    }
)
async def create_label(
    parameters: params.CreateLabel,
    service: LabelService = Depends(get_label_service)
):
    return await service.create_label(parameters)



@router.delete(
    path=Paths.DeleteLabel,
    name="Delete Label",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": responses.Label},
        status.HTTP_404_NOT_FOUND: {},
        status.HTTP_400_BAD_REQUEST: {}
    }
)
async def delete_label(
    id: int,
    service: LabelService = Depends(get_label_service)
):
    return await service.delete_label(id)
