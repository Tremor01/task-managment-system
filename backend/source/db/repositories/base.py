from typing import TypeVar, Generic, Iterable, Any
from abc import ABC, abstractmethod

from ..models.base import Base


ModelT = TypeVar("ModelT", bound=Base)


class AbstractRepository(ABC, Generic[ModelT]):
    
    MODEL: type[ModelT] = None  # type: ignore

    @property
    def model(self) -> type[ModelT]:
        if self.MODEL is None:
            raise ValueError("MODEL not set")
        return self.MODEL
    
    @abstractmethod
    async def execute(self, query: Any) -> Any:
        raise NotImplemented()
    
    @abstractmethod
    async def new(self, **data: Any) -> ModelT | None:
        raise NotImplemented()

    @abstractmethod
    async def create(self, obj: ModelT) -> ModelT | None:
        raise NotImplemented()

    @abstractmethod
    async def update(self, obj: ModelT, **kwargs: Any) -> ModelT | None:
        raise NotImplemented()

    @abstractmethod
    async def delete(self, obj: ModelT):
        raise NotImplemented()
    
    @abstractmethod
    async def filter(self, *where: Any, **filters: Any) -> Iterable[ModelT]:
        raise NotImplemented()

    @abstractmethod
    async def filter_one(self, *where: Any, **filters: Any) -> ModelT | None:
        raise NotImplemented()

    @abstractmethod
    async def count(self, **filters: Any) -> int:
        raise NotImplemented()

    @abstractmethod
    async def select_all(self) -> list[ModelT]:
        raise NotImplemented()