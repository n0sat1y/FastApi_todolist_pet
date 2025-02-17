from pydantic import BaseModel, EmailStr
from datetime import datetime


class TaskAddSchema(BaseModel):
	title: str
	description: str | None = None
	is_done: bool = False
	deadline: datetime | None = None

class TaskSchema(TaskAddSchema):
	id: int

class EmailSchema(BaseModel):
	email: EmailStr

class UserSchema(EmailSchema):
	password: str

class ShowUserSchema(UserSchema):
	id: int

class TokenSchema(BaseModel):
	access_token: str | None = None
	refresh_token: str | None = None
	type: str | None = None

class GetUserIdSchema(BaseModel):
	user_id: int