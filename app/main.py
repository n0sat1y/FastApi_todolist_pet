from fastapi import FastAPI
import uvicorn
from routers.tasks import router as task_router
from routers.users import router as user_router
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
app.include_router(task_router)
app.include_router(user_router)


if __name__ == '__main__':
   uvicorn.run('main:app', reload=True)
