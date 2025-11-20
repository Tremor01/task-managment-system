from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.repositories import BaseRepository, LabelRepository
from db.database import get_session

from schemas.label import *


class LabelService:
    
    def __init__(self, label_repo: BaseRepository):
        self.label_repo: BaseRepository = label_repo
    
    async def create_label(self, parameters: LabelCreateParams) -> LabelResponse:
        await self.label_repo.new(name=parameters.name)
    
    async def get_labels(self, parameters: LabelGetParams) -> list[LabelResponse]:
        await self.label_repo.select_all()
    
    
def get_label_service(session: AsyncSession = Depends(get_session)) -> LabelService:
    repo = LabelRepository(session)
    return LabelService(repo)
