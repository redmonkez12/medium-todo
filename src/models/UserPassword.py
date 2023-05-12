import datetime

from sqlmodel import SQLModel, Field, Relationship

import sqlalchemy as sa

from src.models.User import User


class UserPassword(SQLModel, table=True):
    __tablename__ = "user_passwords"

    user_password_id: int = Field(default=None, primary_key=True)
    value: str = Field(sa_column=sa.Column(sa.TEXT, nullable=False))
    user_id: int = Field(
        sa_column=sa.Column(sa.Integer, sa.ForeignKey(User.user_id, ondelete="CASCADE"), nullable=False))
    created_at: datetime.datetime = Field(sa_column=sa.Column(sa.DateTime(timezone=True), default=datetime.datetime.now))
    updated_at: datetime.datetime = Field(sa_column=sa.Column(sa.DateTime(timezone=True), default=datetime.datetime.now))

    user: User = Relationship(back_populates="passwords")