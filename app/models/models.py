from typing import Annotated
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime, timezone

from core.database import Base


intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(default=datetime.now(timezone.utc))]

class TaskModel(Base):
    __tablename__ = 'tasks'
    
    # Добавляем это, чтобы избежать конфликтов при повторном определении
    __table_args__ = {'extend_existing': True}

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
    
    # Добавляем это, чтобы избежать конфликтов при повторном определении
    __table_args__ = {'extend_existing': True}

    id: Mapped[intpk]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[created_at]

    tasks = relationship('TaskModel', back_populates='user')

    def __repr__(self):
        return f"{self.email}"
