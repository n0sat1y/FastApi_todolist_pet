from typing import Annotated
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime


from core.database import Base

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(default=datetime.utcnow())]

class TaskModel(Base):
	__tablename__ = 'tasks'

	id: Mapped[intpk]
	title: Mapped[str]
	description: Mapped[str | None]
	is_done: Mapped[bool] = mapped_column(default=False)
	deadline: Mapped[datetime | None]
	created_at: Mapped[created_at]
	user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))

	user = relationship('UserModel', back_populates='tasks')

	def __repr__(self):
		return f"{self.id} -- {self.title}"


class UserModel(Base):
	__tablename__ = 'users'

	id: Mapped[intpk]
	email: Mapped[str] = mapped_column(unique=True)
	password: Mapped[str]
	created_at: Mapped[created_at]

	tasks = relationship('TaskModel', back_populates='user')

	def __repr__(self):
		return f"{self.email}"