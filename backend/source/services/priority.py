from fastapi import Depends, HTTPException
from fastapi import status as api_statuses
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.repositories import AbstractRepository, PriorityRepository
from ..db.dbase import get_session

from ..schemas.priority import params, responses


class PriorityService:
    
    def __init__(self, priority_repo: AbstractRepository):
        self.priority_repo: AbstractRepository = priority_repo

    async def create_priority(self, parameters: params.CreatePriority) -> responses.Priority:
        model = await self.priority_repo.new(name=parameters.name)
        if model is None:
            raise HTTPException(status_code=api_statuses.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return responses.Priority.model_validate(model, from_attributes=True)
    
    async def delete_priority(self, priority_id: int) -> responses.Priority:
        model = await self.priority_repo.get_by_id(priority_id)
        if model is None:
            raise HTTPException(status_code=api_statuses.HTTP_404_NOT_FOUND, detail="Priority not found")
        
        status = await self.priority_repo.delete(model)
        return (
            responses.Priority.model_validate(model, from_attributes=True)
            if status else 
            None
        )
    
    async def get_priorities(self, parameters: params.GetPriorities) -> responses.GetPriorities:
        items = list()
        
        db_response = await self.priority_repo.select_all()
        for model in db_response:
            items.append(responses.Priority.model_validate(model, from_attributes=True))
            
        return responses.GetPriorities(items=items)

def get_priority_service(session: AsyncSession = Depends(get_session)) -> PriorityService:
    repo = PriorityRepository(session)
    return PriorityService(repo)
