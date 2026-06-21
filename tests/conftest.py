import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlmodel import SQLModel, StaticPool

from app.database import get_db
from app.main import app


@pytest_asyncio.fixture(name="engine")
async def engine_fixture():
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        poolclass=StaticPool,
    )
    async with engine.begin() as db:
        await db.run_sync(SQLModel.metadata.create_all)
    yield engine


@pytest_asyncio.fixture(name="db")
async def db_fixture(engine):
    async with AsyncSession(engine) as db:
        yield db


@pytest_asyncio.fixture(name="client")
async def client_fixture(engine):
    async def override_get_db():
        async with AsyncSession(engine) as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test", follow_redirects=True
    ) as client:
        yield client
    app.dependency_overrides.clear()
