import pytest
from app.repositories import UserRepository, TaskRepository
from app.schemas import EmailSchema, UserSchema
from fastapi import HTTPException
from pydantic import ValidationError

from app.utils import encode_access_jwt


@pytest.mark.asyncio
async def test_create_user(test_user):
    user = await UserRepository.create_user(test_user)

    assert user.id is not None
    assert user.email == test_user.email

@pytest.mark.asyncio
async def test_create_registered_user(test_user):
    with pytest.raises(HTTPException) as e:
        await UserRepository.create_user(test_user)

    assert e.value.status_code == 403
    assert e.value.detail == 'This user has already been registered'

@pytest.mark.asyncio
async def test_get_user(test_user):
    user = await UserRepository.get_user(test_user.email)
    assert user.id is not None
    assert user.email == test_user.email
    assert user.password is not None

@pytest.mark.asyncio
async def test_get_unregistered_user():
    test_user = EmailSchema(email='test@wrong.ru')
    user = await UserRepository.get_user(test_user.email)
    
    assert user is None

@pytest.mark.asyncio
async def test_login_user(test_user):
    user = await UserRepository.login_user(test_user)
    assert user['access_token'] is not None
    assert user['refresh_token'] is not None

@pytest.mark.asyncio
@pytest.mark.parametrize('user', [
    UserSchema(email='wrong@email.com', password='test'),
    UserSchema(email='test@example.com', password='wrong_password'),
])
async def test_login_wrong_user(user):
    with pytest.raises(HTTPException) as e:
        await UserRepository.login_user(user)
    
    assert e.value.status_code == 401
    assert e.value.detail == 'Invalid username or password'

@pytest.mark.asyncio
async def test_add_task(test_task, test_tokens):
    task = await TaskRepository.add_task(test_task, test_tokens['access_token'])
    assert task.id is not None
    assert task.title == test_task.title
    assert task.description is None
    assert task.user_id == 1

@pytest.mark.asyncio
async def test_add_task_with_wrong_user(test_task):
    token = encode_access_jwt({'sub': '2'})
    with pytest.raises(HTTPException) as e:
        await TaskRepository.add_task(test_task, token)
    
    assert e.value.status_code == 401
    assert e.value.detail == 'User not found'

@pytest.mark.asyncio
async def test_get_user_tasks(test_tokens):
    tasks = await UserRepository.get_tasks(test_tokens['access_token'])
    assert tasks is not None
    assert len(tasks) > 0

@pytest.mark.asyncio
async def test_get_tasks_from_wrong_user():
    token = encode_access_jwt({'sub': '2'})
    with pytest.raises(HTTPException) as e:
        await UserRepository.get_tasks(token)

    assert e.value.status_code == 401
    assert e.value.detail == 'User not found'

@pytest.mark.asyncio
async def test_get_tasks():
    tasks = await TaskRepository.get_tasks()
    assert tasks is not None
    assert len(tasks) > 0
