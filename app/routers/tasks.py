from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from schemas import TaskAddSchema, TaskSchema
from repositories import TaskRepository
from typing import Annotated


router = APIRouter(prefix='/tasks', tags=['Задачи'])
http_bearer = HTTPBearer()

@router.get('', summary='Получить список задач')
async def get_tasks():
	result = await TaskRepository.get_tasks()
	return result


@router.post('', summary='Добавить задачу')
async def add_task(data: Annotated[TaskAddSchema, Depends()], creds: HTTPAuthorizationCredentials = Depends(http_bearer)):
	token = creds.credentials
	result = await TaskRepository.add_task(data, token)
	print(result)
	return {'ok': True, 'task_id': result}