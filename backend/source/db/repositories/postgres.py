import logging

from typing import TypeVar, Generic, Iterable, Any, AsyncGenerator
from contextlib import asynccontextmanager

from asyncpg import InterfaceError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, exc

from .base import BaseRepository
from db.models.base import Base


ModelT = TypeVar("ModelT", bound=Base)


class PostgresRepository(BaseRepository, Generic[ModelT]):
    
    MODEL: type[ModelT] = None  # type: ignore

    def __init__(self, session: AsyncSession):
        self.session = session

    async def execute(self, query: Any) -> Any:
        try:
            async with self._start_session():
                return await self.session.execute(query)
        except (InterfaceError, exc.DBAPIError) as e:
            logging.error(f'Failed to execute: {e}')

    async def new(self, **data: Any) -> ModelT | None:
        try:
            obj = self.model(**data)
            return await self.create(obj)
        except Exception as e:
            logging.error(f"Failed to create {self.model.__name__}: {e}")
        return None

    async def create(self, obj: ModelT) -> ModelT | None:
        async with self._start_session():
            self.session.add(obj)
            
            status = self._try_commit()
            if not status:
                return None
            
            await self.session.refresh(obj)
            
        return obj

    async def _try_commit(self) -> bool:
        try:
            await self.session.commit()
            return True
        
        except exc.IntegrityError as e:
            logging.error(e)
            await self.rollback()
            
        return False
    
    async def update(self, obj: ModelT, **kwargs: Any) -> ModelT | None:
        async with self._start_session():
            for key, value in kwargs.items():
                setattr(obj, key, value)
                
            status = self._try_commit()
            if not status:
                return None
            
        async with self._start_session():
            await self.session.refresh(obj)
            
        return obj

    async def delete(self, obj: ModelT) -> bool:
        async with self._start_session():
            try:
                await self.session.delete(obj)
                await self.commit()
                return True
            except Exception as e:
                logging.error(f"Delete failed for {self.model.__name__}: {e}")
                await self.session.rollback()
                return False
    
    async def get_by_id(self, id: int) -> ModelT | None:
        async with self._start_session():
            return await self.filter_one(self.model.id == id)

    async def filter(self, *where: Any, **filters: Any) -> Iterable[ModelT]:
        query = self._get_query().where(*where).filter_by(**filters)
        return (await self.execute(query)).scalars()

    async def filter_one(self, *where: Any, **filters: Any) -> ModelT | None:
        query = self._get_query().where(*where).filter_by(**filters)
        return (await self.execute(query)).scalar_one_or_none()

    async def count(self, **filters: Any) -> int:
        query = self._get_query(func.count(self.model.id)).filter_by(**filters)
        return (await self.execute(query)).scalar_one()

    def _get_query(self, select_data: Any = None):
        if select_data is None:
            select_data = self.model
        return select(select_data)

    @asynccontextmanager
    async def _start_session(self) -> AsyncGenerator[AsyncSession, None]:
        if self.session.is_active:
            yield self.session
            return
        
        async with self.session.begin():
            yield self.session

    async def select_all(self) -> list[ModelT]:
        models = (await self.execute(self._get_query())).scalars().all()
        return list(models)

