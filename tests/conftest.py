from datetime import datetime, timezone
import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.core.database import engine, Base, new_session
from app.schemas import TaskSchema, UserSchema


@pytest.fixture(scope='session', autouse=True)
async def start_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def session_rollback():
    async with new_session() as session:
        transaction = await session.begin()
        yield transaction
        await transaction.rollback()

@pytest.fixture
async def test_user():
    return UserSchema(
        email='test@example.com',
        password='test'
    )

@pytest.fixture
async def test_task():
    return TaskSchema(
        title='Task',
        deadline=datetime.now(timezone.utc)
    )