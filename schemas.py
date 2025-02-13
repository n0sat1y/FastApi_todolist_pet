from pydantic import BaseModel
from datetime import datetime


class TaskAddSchema(BaseModel):
	title: str
	description: str | None = None
	is_done: bool | None = False
	deadline: datetime | None = None


class TaskSchema(TaskAddSchema):
	id: int