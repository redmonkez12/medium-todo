import datetime
from typing import Optional

from sqlmodel import SQLModel, Field

import sqlalchemy as sa


class Todo(SQLModel, table=True):
    __tablename__ = "todos"

    id: Optional[int] = Field(default=None, primary_key=True)
    value: str = Field(sa_column=sa.Column(sa.TEXT, nullable=False, unique=True))
    created_at: datetime.datetime = Field(sa_column=sa.Column(sa.DateTime(timezone=True), default=datetime.datetime.now))
