from fastapi import APIRouter


router = APIRouter(prefix='/tasks', tags=['Задачи'])

@router.get('', summary='Получить список задач')
async def get_tasks():
	return []