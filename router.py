from fastapi import APIRouter


router = APIRouter(
	prefix='/tasks',
	tags=['Задачи']
)

@router.get('', summary='Получить все задачи')
async def get_tasks():
	return []