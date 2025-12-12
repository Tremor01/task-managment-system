from fastapi import Depends, HTTPException
from fastapi import status as api_statuses

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

from ..db.repositories import AbstractRepository, LabelRepository
from ..db.dbase import get_session

from ..schemas.label import params, responses


class LabelService:
    
    def __init__(self, label_repo: AbstractRepository):
        self.label_repo: AbstractRepository = label_repo
    
    async def create_label(self, parameters: params.CreateLabel) -> responses.Label:
        model = await self.label_repo.new(name=parameters.name)
        if model is None:
            raise HTTPException(status_code=api_statuses.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return responses.Label.model_validate(model, from_attributes=True)
    
    async def get_labels(self, parameters: params.GetLabels) ->  responses.GetLabels:
        items = list()
        
        db_response = await self.label_repo.select_all()
        for model in db_response:
            items.append(responses.Label.model_validate(model, from_attributes=True))
            
        return responses.GetLabels(items=items)
    
    async def delete_label(self, label_id: int) -> responses.Label:
        model = await self._get_lable_by_id(label_id) 
        status = await self.label_repo.delete(model)
        return model if status else None
    
    async def update_label(self, parameters: params.UpdateLabel, label_id: int) -> responses.Label:
        model = await self._get_lable_by_id(label_id)
        
        updated_model = await self.label_repo.update(model, **parameters.model_dump())
        if not updated_model:
            raise HTTPException(status_code=api_statuses.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return responses.Label.model_validate(updated_model, from_attributes=True)
    
    async def _get_lable_by_id(self, label_id: int) -> Any:
        model = await self.label_repo.get_by_id(label_id)
        if model is None:
            raise HTTPException(status_code=api_statuses.HTTP_404_NOT_FOUND, detail="Label not found")
        return model

    
def get_label_service(session: AsyncSession = Depends(get_session)) -> LabelService:
    repo = LabelRepository(session)
    return LabelService(repo)
