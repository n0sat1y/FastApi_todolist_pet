from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routers.tasks import router as task_router
from routers.users import router as user_router
from core.database import create_tables, delete_tables

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
   await create_tables()
   print("База готова")
   yield
   await delete_tables()
   print("База очищена")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost",
]

app = FastAPI(lifespan=lifespan)
app.include_router(task_router)
app.include_router(user_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == '__main__':
   uvicorn.run('main:app', reload=True)
