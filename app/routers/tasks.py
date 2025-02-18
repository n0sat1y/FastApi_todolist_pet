from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from utils import decode_jwt, validate_token_type
from schemas import TaskAddSchema, TaskSchema, GetTasksSchema
from repositories import TaskRepository
from typing import Annotated


router = APIRouter(prefix='/tasks', tags=['Задачи'])
http_bearer = HTTPBearer()

@router.get('', summary='Получить список задач', response_model=list[GetTasksSchema])
async def get_tasks():
	result = await TaskRepository.get_tasks()
	response = [GetTasksSchema.model_validate(item, from_attributes=True) for item in result]
	return response


@router.post('', summary='Добавить задачу', response_model=GetTasksSchema)
async def add_task(data: Annotated[TaskAddSchema, Depends()], creds: HTTPAuthorizationCredentials = Depends(http_bearer)):
	token = creds.credentials
	validate_token_type(decode_jwt(token), 'access')
	result = await TaskRepository.add_task(data, token)
	print(result)
	return GetTasksSchema.model_validate(result, from_attributes=True)