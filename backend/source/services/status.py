from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.repositories import BaseRepository, StatusRepository
from db.database import get_session

from schemas.status import params
from typing import Any


class StatusService:
    
    def __init__(self, status_repo: BaseRepository):
        self.status_repo: BaseRepository = status_repo
        
    async def create_status(self, parametes: params.CreateStatus) -> Any:
        await self.status_repo.new(name=parametes.name)
    

def get_status_service(session: AsyncSession = Depends(get_session)) -> StatusService:
    repo = StatusRepository(session)
    return StatusService(repo)
