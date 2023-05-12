from pydantic import BaseModel


class CreateTodoRequest(BaseModel):
    value: str
