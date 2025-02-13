from fastapi import FastAPI
from router import router
from database import create_tables, delete_tables

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
	await delete_tables()
	print('Бд удалена')
	await create_tables()
	print('Бд создана')
	yield

app = FastAPI(lifespan=lifespan)
app.include_router(router=router)