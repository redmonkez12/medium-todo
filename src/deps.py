from src.database import async_session
from src.services.TodoService import TodoService
from src.services.UserService import UserService


async def get_todo_service():
    async with async_session() as session:
        async with session.begin():
            yield TodoService(session)


async def get_user_service():
    async with async_session() as session:
        async with session.begin():
            yield UserService(session)
