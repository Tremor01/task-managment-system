from fastapi import Depends, HTTPException
from fastapi import status as api_statuses

from sqlalchemy.ext.asyncio import AsyncSession

from db.repositories import BaseRepository, StatusRepository
from db.database import get_session

from schemas.status import params, responses


class StatusService:
    
    def __init__(self, status_repo: BaseRepository):
        self.status_repo: BaseRepository = status_repo
        
    async def create_status(self, parametes: params.CreateStatus) -> responses.Status:
        model = await self.status_repo.new(name=parametes.name)
        if model is None:
            raise HTTPException(status_code=api_statuses.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return responses.Status.model_validate(model, from_attributes=True)
        
    async def delete_status(self, status_id: int) -> responses.Status:
        model = await self.status_repo.get_by_id(status_id)
        if model is None:
            raise HTTPException(status_code=api_statuses.HTTP_404_NOT_FOUND, detail="Status not found")
        
        status = await self.status_repo.delete(model)
        if not status:
            raise HTTPException(status_code=api_statuses.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return responses.Status.model_validate(model, from_attributes=True)

    async def get_statuses(self, parameters: params.GetStatuses) ->  responses.GetStatuses:
        items = list()
        
        db_response = await self.status_repo.select_all()
        for model in db_response:
            items.append(responses.Status.model_validate(model, from_attributes=True))
            
        return responses.GetStatuses(items=items)
    

def get_status_service(session: AsyncSession = Depends(get_session)) -> StatusService:
    repo = StatusRepository(session)
    return StatusService(repo)
