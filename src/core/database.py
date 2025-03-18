from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from .settings import settings


class Base(DeclarativeBase):
    """Базовая модель, от которой наследуются остальные модели."""

    pass


async_engine = create_async_engine(
    url=settings.async_database_url,
    pool_size=5,
    max_overflow=10,
)

async_session = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронный генератор для сессии."""
    async with async_session() as session:
        yield session
