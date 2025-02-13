from database import session, TaskModel
from sqlalchemy import select

from schemas import TaskAddSchema


class TaskRepository:
	@classmethod
	async def get_tasks(cls):
		async with session() as sess:
			data = select(TaskModel)
			result = await sess.execute(data)
			task_model = result.scalars().all()
			print(task_model)
			return task_model
		
	@classmethod
	async def add_task(cls, data: TaskAddSchema):
		async with session() as sess:
			task_dict = data.model_dump()
			task = TaskModel(**task_dict)
			sess.add(task)
			await sess.flush()
			await sess.commit()
			return task.id