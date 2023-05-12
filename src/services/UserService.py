from datetime import datetime

from sqlmodel import Session, select
from sqlalchemy import exc

from src.auth.password import get_password_hash, verify_password
from src.exceptions.EmailDuplicationException import EmailDuplicationException
from src.exceptions.InvalidData import InvalidData
from src.exceptions.UserNotFoundException import UserNotFoundException
from src.exceptions.UsernameDuplicationException import UsernameDuplicationException
from src.models.User import User
from src.models.UserPassword import UserPassword
from src.requests.CreateUserRequest import CreateUserRequest
from src.requests.LoginRequest import LoginRequest


class UserService:
    def __init__(self, session: Session):
        self.session = session

    async def create_user(self, data: CreateUserRequest):
        try:
            new_user = User(
                first_name=data.first_name,
                last_name=data.last_name,
                email=data.email,
                birthdate=datetime.strptime(data.birthdate, "%d-%m-%Y").date(),
                username=data.username,
                passwords=[UserPassword(value=get_password_hash(data.password))],
            )

            self.session.add(new_user)
            await self.session.commit()

            return new_user
        except exc.IntegrityError as e:
            print(e)
            error_message = str(e.orig)
            if "duplicate key value violates unique constraint" in error_message:
                if "email" in error_message:
                    raise EmailDuplicationException(f"Email [{data.email}] already exists")
                elif "username" in error_message:
                    raise UsernameDuplicationException(f"Username [{data.username}] already exists")
            raise InvalidData("Invalid data")
        except Exception as e:
            print(e)
            raise Exception(e)

    async def get_by_username(self, username: str):
        query = (
            select(User.user_id, User.username, User.email, UserPassword.value.label("password"))
            .join(UserPassword)
            .where(User.username == username)
            .limit(1)
        )

        result = await self.session.execute(query)
        return result.first()

    async def login(self, data: LoginRequest):
        user = await self.get_by_username(data.username)

        if not user:
            raise UserNotFoundException("Username or password is invalid")

        if not verify_password(data.password, user.password):
            raise UserNotFoundException("Username or password is invalid")

        return user
