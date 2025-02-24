from typing import Optional, List
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from core.database import new_session
from models.models import TaskModel, UserModel
from schemas import EmailSchema, GetUserIdSchema, TaskAddSchema, TaskSchema, UserSchema
from utils import decode_jwt, encode_access_jwt, encode_refresh_jwt, hash_password, validate_password

class TaskRepository:
    @classmethod
    async def get_tasks(cls) -> List[TaskSchema]:
        try:
            async with new_session() as sess:
                query = select(TaskModel)
                result = await sess.execute(query)
                return result.scalars().all()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )

    @classmethod
    async def add_task(cls, task_data: TaskAddSchema, token: str) -> TaskModel:
        try:
            async with new_session() as sess:
                user = await UserRepository.get_user_by_token(token)
                user_id = user.id
                task_dict = task_data.model_dump()
                task = TaskModel(**task_dict, user_id=user_id)
                sess.add(task)
                await sess.commit()
                await sess.refresh(task)
                return task
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )

class UserRepository:
    @classmethod
    async def get_user_by_token(cls, token):
        user_id = int(decode_jwt(token).get('sub'))
        user = await UserRepository.get_user(user_id=GetUserIdSchema(user_id=user_id))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='User not found')
        return user

    @classmethod
    async def get_user(cls, 
                       user: EmailSchema = None, 
                       user_id: GetUserIdSchema = None) -> Optional[UserModel]:
        try:
            async with new_session() as session:
                if user_id:
                    query = select(UserModel).where(UserModel.id == user_id.user_id)
                elif user:
                    query = select(UserModel).where(UserModel.email == user)
                else:
                    raise ValueError('Either email or id must be provided')
                result = await session.execute(query)
                return result.scalars().first()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )

    @classmethod
    async def create_user(cls, user: UserSchema) -> UserModel:
        try:
            async with new_session() as session:
                if await cls.get_user(user.email):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail='This user has already been registered'
                    )
                
                hashed_password = hash_password(user.password)
                new_user = UserModel(
                    email=user.email,
                    password=hashed_password
                )
                session.add(new_user)
                await session.commit()
                await session.refresh(new_user)
                return new_user
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )

    @classmethod
    async def login_user(cls, user: UserSchema) -> dict:
        try:
            async with new_session() as session:
                auth_error = HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Invalid username or password'
                )
                
                model_user = await cls.get_user(user.email)
                if not model_user:
                    raise auth_error

                if not validate_password(user.password, model_user.password):
                    raise auth_error

                payload = {'sub': str(model_user.id)}
                return {
                    'access_token': encode_access_jwt(payload),
                    'refresh_token': encode_refresh_jwt(payload)
                }
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )

    @classmethod
    async def get_tasks(cls, token: str) -> List[TaskModel]:
        try:
            async with new_session() as sess:
                user = await UserRepository.get_user_by_token(token)
                user_id = user.id
                query = (
                    select(TaskModel)
                    .filter_by(user_id=user_id)
                    .options(selectinload(TaskModel.user))
                )
                result = await sess.execute(query)
                return result.scalars().all()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )
