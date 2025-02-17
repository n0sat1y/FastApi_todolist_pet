from fastapi import APIRouter, Depends
from schemas import TaskAddSchema, TaskSchema
from repositories import TaskRepository
from typing import Annotated


router = APIRouter(prefix='/tasks', tags=['Задачи'])

@router.get('', summary='Получить список задач')
async def get_tasks():
	result = await TaskRepository.get_tasks()
	return result


@router.post('', summary='Добавить задачу')
async def add_task(data: Annotated[TaskAddSchema, Depends()]):
	result = await TaskRepository.add_task(data)
	print(result)
	return {'ok': True, 'task_id': result}