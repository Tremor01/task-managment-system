from typing import Any
from fastapi import Depends, HTTPException
from fastapi import status as api_statuses

from sqlalchemy.ext.asyncio import AsyncSession

from db.repositories import BaseRepository, LabelRepository
from db.database import get_session

from schemas.label import params


class LabelService:
    
    def __init__(self, label_repo: BaseRepository):
        self.label_repo: BaseRepository = label_repo
    
    async def create_label(self, parameters: params.CreateLabel) -> Any:
        return await self.label_repo.new(name=parameters.name)
    
    async def get_labels(self, parameters: params.GetLabels) -> Any:
        return await self.label_repo.select_all()
    
    async def delete_label(self, parameters: params.DeleteLabel) -> Any:
        model = self.label_repo.get_by_id(parameters.label_id)
        if model is None:
            raise HTTPException(status_code=api_statuses.HTTP_404_NOT_FOUND, detail="Label not found")
        
        status = await self.label_repo.delete()
        return model if status else None
    
    
def get_label_service(session: AsyncSession = Depends(get_session)) -> LabelService:
    repo = LabelRepository(session)
    return LabelService(repo)
