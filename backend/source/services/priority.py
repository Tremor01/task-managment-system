from typing import Any
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.repositories import BaseRepository, PriorityRepository
from db.database import get_session

from schemas.priority import params


class PriorityService:
    
    def __init__(self, priority_repo: BaseRepository):
        self.priority_repo: BaseRepository = priority_repo

    async def create_priority(self, parameters: params.CreatePriority) -> Any:
        return await self.priority_repo.new(name=parameters.name)
    

def get_priority_service(session: AsyncSession = Depends(get_session)) -> PriorityService:
    repo = PriorityRepository(session)
    return PriorityService(repo)
