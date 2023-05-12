from fastapi import Body, Response, status, HTTPException, Depends, Query, APIRouter
from typing import Annotated
from sqlalchemy.exc import NoResultFound

from src.auth.user import get_current_user
from src.deps import get_todo_service
from src.models.Todo import Todo
from src.requests.CreateTodoRequest import CreateTodoRequest
from src.requests.UpdateTodoRequest import UpdateTodoRequest
from src.responses.GetByUsernameResponse import GetByUsernameResponse
from src.services.TodoService import TodoService

todo_router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)


@todo_router.get("/", response_model=list[Todo])
async def get_todos(*,
                    todo_service: TodoService = Depends(get_todo_service),
                    offset: Annotated[int | None, Query()] = 0,
                    limit: Annotated[int | None, Query()] = 10,
                    current_user: GetByUsernameResponse = Depends(get_current_user),
                    ):
    print(current_user)  # @TODO We will use this later

    todo_list = await todo_service.get_todos(offset, limit)

    return todo_list


@todo_router.get("/{todo_id}", response_model=Todo)
async def get_todo(*,
                   todo_service: TodoService = Depends(get_todo_service),
                   todo_id: int
                   ):
    try:
        return await todo_service.get_todo(todo_id)
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={
                                "message": f"Todo [{todo_id}] not found",
                                "status_code": status.HTTP_404_NOT_FOUND,
                                "code": "TODO_NOT_FOUND",
                            })
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={
                                "message": "Something went wrong",
                                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                                "code": "INTERNAL_SERVER_ERROR",
                            })


@todo_router.post("/", response_model=Todo)
async def create_todo(*, data: CreateTodoRequest = Body(), todo_service: TodoService = Depends(get_todo_service)):
    new_todo = await todo_service.create_todo(data)

    return new_todo


@todo_router.patch("/", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(*, todo: UpdateTodoRequest = Body(),
                      todo_service: TodoService = Depends(get_todo_service), ):
    await todo_service.update_todo(todo)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@todo_router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(*, todo_id: int, todo_service: TodoService = Depends(get_todo_service)):
    await todo_service.delete_todo(todo_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
