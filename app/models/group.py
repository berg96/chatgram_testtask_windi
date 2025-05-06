from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class Group(Base):
    id: Mapped[UUID] = mapped_column(
        ForeignKey('chats.id', ondelete='CASCADE'), primary_key=True
    )
    creator_id: Mapped[UUID] = mapped_column(
        ForeignKey('user.id'), nullable=False
    )

    chat: Mapped['Chat'] = relationship(
        back_populates='group', single_parent=True
    )
