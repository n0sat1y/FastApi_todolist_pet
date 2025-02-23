import pytest
from app.repositories import UserRepository, TaskRepository
from app.schemas import EmailSchema, UserSchema
from fastapi import HTTPException
from pydantic import ValidationError


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
