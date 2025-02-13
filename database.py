from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


engine = create_async_engine(
	url='sqlite+aiosqlite:///tasks.db'
)
session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
	pass


class TaskModel(Base):
	__tablename__ = 'tasks'

	id: Mapped[int] = mapped_column(primary_key=True)
	title: Mapped[str]
	description: Mapped[str]
	is_done: Mapped[bool] = mapped_column(default=False)
	deadline: Mapped[datetime | None]
	created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())


async def create_tables():
	async with engine.connect() as conn:
		await conn.run_sync(Base.metadata.create_all)


async def delete_tables():
	async with engine.connect() as conn:
		await conn.run_sync(Base.metadata.drop_all)