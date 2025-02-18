from core.database import new_session
from models import TaskModel, UserModel
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from schemas import EmailSchema, TaskAddSchema, TaskSchema, UserSchema
from utils import decode_jwt, encode_access_jwt, encode_refresh_jwt, hash_password, validate_password


class TaskRepository:
	@classmethod
	async def get_tasks(cls) -> list[TaskSchema]:
		async with new_session() as sess:
			data = select(TaskModel)
			result = await sess.execute(data)
			task_model = result.scalars().all()
			return task_model
		
	@classmethod
	async def add_task(cls, task_data: TaskAddSchema, token: str) -> int:
		async with new_session() as sess:
			user = int(decode_jwt(token).get('sub'))
			task_dict = task_data.model_dump()
			task = TaskModel(**task_dict, user_id=user)
			sess.add(task)
			await sess.flush()
			await sess.commit()
			return task
		
class UserRepository:
	@classmethod
	async def get_user(cls, user: EmailSchema):
		async with new_session() as session:
			try:
				query = select(UserModel).where(UserModel.email==user)
				result = await session.execute(query)
				model_user = result.scalars().first()
				return model_user
			except:
				raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')


	@classmethod
	async def create_user(cls, user: UserSchema):
		async with new_session() as session:
			result = await cls.get_user(user.email)
			if result:
				raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='This user has already been registered')
			email: str = user.email
			password: bytes = hash_password(user.password)
			user = UserModel(email=email, password=password)
			session.add(user)
			await session.commit()
			await session.refresh(user)
			return user
		
	@classmethod
	async def login_user(cls, user: UserSchema):
		async with new_session() as session:
			exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверное имя пользователя или пароль')
			model_user = await cls.get_user(user.email)
			if not model_user:
				raise exc
			if not validate_password(user.password, model_user.password):
				raise exc
			payload = {'sub': str(model_user.id)}
			access_token = encode_access_jwt(payload)
			refresh_token = encode_refresh_jwt(payload)
			return {'access_token': access_token, 'refresh_token': refresh_token}
		

	@classmethod
	async def get_tasks(cls, token):
		async with new_session() as sess:
			decoded_token = decode_jwt(token)
			user_id = int(decoded_token.get('sub'))
			get_tasks = await sess.execute(select(TaskModel).filter_by(user_id=user_id))
			return get_tasks.scalars().all()