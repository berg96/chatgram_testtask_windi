from typing import List
from uuid import UUID

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.constants import MAX_LENGTH_CHAT_NAME
from core.db import Base
import enum


class ChatType(str, enum.Enum):
    private = 'private'
    group   = 'group'


class Chat(Base):
    name: Mapped[str] = mapped_column(
        String(MAX_LENGTH_CHAT_NAME), nullable=False
    )
    type: Mapped[ChatType] = mapped_column(
        Enum(ChatType), nullable=False, default=ChatType.private
    )

    members: Mapped[List['User']] = relationship(
        secondary='chatmembers', back_populates='chats'
    )
    messages: Mapped[List['Message']] = relationship(back_populates='chat')
    group: Mapped['Group'] = relationship(
        'Group', back_populates='chat', uselist=False
    )


class ChatMember(Base):
    chat_id: Mapped[UUID] = mapped_column(
        ForeignKey('chats.id', ondelete='CASCADE'), primary_key=True
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey('user.id', ondelete='CASCADE'), primary_key=True
    )
