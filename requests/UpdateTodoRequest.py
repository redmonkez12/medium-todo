from pydantic import BaseModel


class UpdateTodoRequest(BaseModel):
    id: int
    value: str
