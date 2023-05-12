from sqlmodel import SQLModel

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values

from settings import Settings

settings = Settings()

config = dotenv_values("./.env")
username = settings.DB_USERNAME
password = settings.DB_PASSWORD
dbname = settings.DB_NAME

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{username}:{password}@localhost:5432/{dbname}"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
