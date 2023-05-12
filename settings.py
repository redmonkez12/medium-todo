from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_NAME : str
    DB_PASSWORD: str
    DB_USERNAME: str
    SECRET_KEY: str

# specify .env file location as Config attribute
    class Config:
        env_file = ".env-test"
