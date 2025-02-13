from pydantic import BaseModel
from datetime import datetime


class TaskAddSchema(BaseModel):
	title:  str
	description: str | None
	deadline: datetime | None


class TasksSchema(TaskAddSchema):
	id: int