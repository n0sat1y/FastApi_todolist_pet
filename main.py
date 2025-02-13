from fastapi import FastAPI
from router import router
from database import create_tables, drop_tables

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
	drop_tables()
	print('Бд удалена')
	create_tables()
	print('Бд создана')
	#ok
	yield


app = FastAPI()
app.include_router(router)


