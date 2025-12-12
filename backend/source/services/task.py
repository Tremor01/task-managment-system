from fastapi import Depends, HTTPException
from fastapi import status as api_statuses

from sqlalchemy.ext.asyncio import AsyncSession

from ..db.repositories import AbstractRepository, TaskRepository
from ..db.dbase import get_session

from ..schemas.task import params, responses


class TaskService:
    
    def __init__(self, task_repo: AbstractRepository):
        self.task_repo = task_repo
    
    async def get_tasks(self, parameters: params.GetTasks) -> responses.GetTasks:
        items = list()
        
        db_response = await self.task_repo.get_tasks(parameters)
        for model in db_response:
            items.append(
                responses.Task.model_validate(model, from_attributes=True)
            )
            
        return responses.GetTasks(items=items)
    
    async def create_task(self, parameters: params.CreateTask) -> responses.Task:
        model = await self.task_repo.new(**parameters.model_dump())
        if model is None:
            raise HTTPException(status_code=api_statuses.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return responses.Task.model_validate(model, from_attributes=True)
    
    async def delete_task(self, task_id: int) -> responses.Task:
        model = await self._get_model_task_by_id(task_id)
        
        status = await self.task_repo.delete(model)
        if not status:
            raise HTTPException(status_code=api_statuses.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return responses.Task.model_validate(model, from_attributes=True)
    
    async def update_task(self, parameters: params.UpdateTask, task_id: int) -> responses.Task:
        model = await self._get_model_task_by_id(task_id)
        
        updated_model = await self.task_repo.update(model, **parameters.model_dump())
        if not updated_model:
            raise HTTPException(status_code=api_statuses.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return responses.Task.model_validate(updated_model, from_attributes=True)
    
    async def _get_model_task_by_id(self, task_id: int):
        model = await self.task_repo.get_by_id(task_id)
        if model is None:
            raise HTTPException(status_code=api_statuses.HTTP_404_NOT_FOUND, detail="Task not found")
        
        return model
    
    
def get_task_service(session: AsyncSession = Depends(get_session)) -> TaskService:
    repo = TaskRepository(session)
    return TaskService(repo)
