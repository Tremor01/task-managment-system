from .postgres import PostgresRepository
from db.models import Task
from typing import Any

from schemas.task import params


class TaskRepository(PostgresRepository[Task]):
    MODEL = Task

    async def get_tasks(self, parameters: params.GetTasks) -> Any:
        await self.select_all()
    
    async def create_task(self, parameters: params.CreateTask) -> Any:
        model = await self.new(**parameters)
        return model
        
    async def update_task(self, parameters: params.UpdateTask) -> Any:
        ...
    
    