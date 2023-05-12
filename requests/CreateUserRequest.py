from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    birthdate: str
    username: str
    password: str
