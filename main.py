from fastapi import FastAPI
from router import router
from database import create_tables, delete_tables

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
   await create_tables()
   print("База готова")
   yield
   await delete_tables()
   print("База очищена")

app = FastAPI(lifespan=lifespan)
app.include_router(router=router)
