from __future__ import annotations

from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from testcontainers.postgres import PostgresContainer

from src.adapters.out.postgres.database import Base, Database


@pytest.fixture(scope="session")
def postgres_url() -> str:
    with PostgresContainer("postgres:16", driver="asyncpg") as pg:
        yield pg.get_connection_url()


@pytest_asyncio.fixture
async def database(postgres_url: str) -> AsyncGenerator[Database, None]:
    db = Database(url=postgres_url)
    engine = db._engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield db

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await db.dispose()


@pytest_asyncio.fixture
async def db_session(database: Database) -> AsyncGenerator[AsyncSession, None]:
    session = database.session_factory()
    try:
        yield session
    finally:
        await session.rollback()
        await session.close()
