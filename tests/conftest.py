from typing import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src.core.database import Base, get_session
from src.core.settings import settings
from src.main import app

async_engine = create_async_engine(
    url=settings.async_test_database_url,
    poolclass=NullPool,
)


async def override_get_session():
    """Фиктивная сессия для тестов."""
    async_session = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session
        await session.close()


app.dependency_overrides[get_session] = override_get_session


@pytest_asyncio.fixture(scope='function', autouse=True)
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Асинхронный клиент."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as ac:
        yield ac


@pytest_asyncio.fixture(scope='session', autouse=True)
async def setup_database():
    """Подготовка базы данных перед тестами."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
