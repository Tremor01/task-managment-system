from pydantic import PostgresDsn
from typing import AsyncIterator, no_type_check

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from .settings import get_db_settings


Base = declarative_base()


DB_SCHEME = "postgresql+asyncpg"
DB_SETTINGS = get_db_settings()


DATABASE_URL = PostgresDsn.build(  # type: ignore
    scheme=DB_SCHEME,
    username=DB_SETTINGS.user,
    password=DB_SETTINGS.password,
    host=DB_SETTINGS.host,
    port=int(DB_SETTINGS.port),
    path=DB_SETTINGS.db_name,
)

ENGINE = create_async_engine(url=str(DATABASE_URL), 
                             pool_pre_ping=True,
                             future=True)


async def init_db():
    async with ENGINE.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


@no_type_check
async def get_session() -> AsyncIterator[AsyncSession]:
    async_session = sessionmaker(
        bind=ENGINE,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session


async def create_db_and_tables():
    async with ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
