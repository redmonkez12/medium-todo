from fastapi import FastAPI

from src.controllers.AuthController import auth_router
from src.controllers.TodoController import todo_router
from src.database import init_db


app = FastAPI()


@app.get("/")
async def index():
    return "Api is running"


@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(auth_router, prefix="/api/v1")
app.include_router(todo_router, prefix="/api/v1")
