from fastapi import APIRouter, Depends, status
from .api_settings import Paths, PREFIX

from schemas.task import responses, params
from services import TaskService, get_task_service


TAGS = ["Tasks"]
router = APIRouter(prefix=PREFIX, tags=TAGS)  # type: ignore


@router.get(
    path=Paths.GetTask,
    name="Get Task",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": responses.GetTasks},
        status.HTTP_404_NOT_FOUND: {},
        status.HTTP_400_BAD_REQUEST: {}
    }
)
async def get_task(
    parameters: params.GetTasks = Depends(),
    service: TaskService = Depends(get_task_service)
):
    return await service.get_tasks(parameters)


@router.post(
    path=Paths.CreateTask,
    name="Create Task",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": responses.CreateTask},
        status.HTTP_404_NOT_FOUND: {},
        status.HTTP_400_BAD_REQUEST: {}
    }
)
async def get_task(
    parameters: params.CreateTask = Depends(),
    service: TaskService = Depends(get_task_service)
):
    return await service.create_task(parameters)

