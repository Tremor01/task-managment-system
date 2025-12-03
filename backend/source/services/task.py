from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.repositories import BaseRepository, TaskRepository
from db.database import get_session

from schemas.task import responses, params


class TaskService:
    
    def __init__(self, task_repo: BaseRepository):
        self.task_repo = task_repo
    
    async def get_tasks(self, parameters: params.GetTasks) -> responses.GetTasks:
        db_response = await self.task_repo.get_tasks(parameters)
    
    async def create_task(self, parameters: params.CreateTask):
        ...
    
    
def get_task_service(session: AsyncSession = Depends(get_session)) -> TaskService:
    repo = TaskRepository(session)
    return TaskService(repo)
