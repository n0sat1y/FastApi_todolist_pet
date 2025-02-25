from datetime import datetime, timezone
from httpx import ASGITransport, AsyncClient
import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.core.database import engine, Base, new_session
from app.repositories import UserRepository
from app.schemas import TaskAddSchema, TaskSchema, UserSchema
from app.main import app


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
    return TaskAddSchema(
        title='Task',
        deadline=datetime.now(timezone.utc)
    )

@pytest.fixture
async def test_tokens(test_user):
    tokens = await UserRepository.login_user(test_user)
    return tokens

@pytest.fixture
async def client():
    async with AsyncClient(
		transport=ASGITransport(app=app),
		base_url='http://test'
	) as client:
        yield client