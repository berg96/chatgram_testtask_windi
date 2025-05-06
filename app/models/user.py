from typing import List
from uuid import UUID

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.constants import MAX_LENGTH_USER_NAME
from core.db import Base


class User(SQLAlchemyBaseUserTable[UUID], Base):
    name: Mapped[str] = mapped_column(
        String(MAX_LENGTH_USER_NAME), nullable=False
    )

    chats: Mapped[List['Chat']] = relationship(
        secondary='chatmembers', back_populates='members'
    )
    messages: Mapped[List['Message']] = relationship(back_populates='sender')