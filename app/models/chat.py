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
    type: Mapped[ChatType] = mapped_column(Enum(ChatType), nullable=False)

    members: Mapped[List['User']] = relationship(
        secondary='chatmembers', back_populates='chat'
    )
    messages: Mapped[List['Message']] = relationship(back_populates='chat')


class ChatMember(Base):
    chat_id: Mapped[UUID] = mapped_column(
        ForeignKey('chats.id', ondelete='CASCADE'), nullable=False
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey('user.id', ondelete='CASCADE'), nullable=False
    )

    chat: Mapped['Chat'] = relationship(back_populates='members')
    members: Mapped['User'] = relationship(back_populates='chats')
