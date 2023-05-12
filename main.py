from fastapi import FastAPI

from controllers.AuthController import auth_router
from controllers.TodoController import todo_router
from database import init_db


app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(auth_router, prefix="/api/v1")
app.include_router(todo_router, prefix="/api/v1")
