from .postgres import BaseRepository
from ..models import Task, Priority, Label, Status

from ...schemas.task import params

from sqlalchemy import select


class TaskRepository(BaseRepository[Task]):
    MODEL = Task

    async def get_tasks(self, parameters: params.GetTasks):
        query = (
            select(
                Task.id, 
                Task.deadline,
                Task.description,
                Task.created_at,
                
                Priority.name.label('priority'),
                Label.name.label('label'),
                Status.name.label('status'),
            )
            .join(Priority, Priority.id == Task.priority_id)
            .join(Label, Label.id == Task.label_id)
            .join(Status, Status.id == Task.status_id)
        )
        if parameters.label is not None:
            query = query.where(Label.name == parameters.label)
            
        if parameters.priority is not None:
            query = query.where(Priority.name == parameters.priority)
            
        if parameters.status is not None:
            query = query.where(Status.name == parameters.status)
        
        result = await self.execute(query)
        return result.fetchall()
    