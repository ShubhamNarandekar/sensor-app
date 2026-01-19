import pytest
import httpx
from sensor_service.main import app
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sensor_service.utils.config import settings
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="function")
async def async_client():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://127.0.0.1:8000/api/v1") as async_client:
        yield async_client

@pytest.fixture(scope="function")
async def db_session():
    db_engine = create_async_engine(
        settings.db_connection,
        echo=True,
        pool_size=5,
        max_overflow=10
    )

    AsyncSessionTest = sessionmaker(
        bind=db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with AsyncSessionTest() as db_session:
        yield db_session