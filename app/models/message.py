from datetime import datetime
from uuid import UUID
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.db import Base


class Message(Base):
    chat_id: Mapped[UUID] = mapped_column(
        ForeignKey('chats.id'), nullable=False
    )
    sender_id: Mapped[UUID] = mapped_column(
        ForeignKey('user.id'), nullable=False
    )
    text: Mapped[str] = mapped_column(nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    is_read: Mapped[bool] = mapped_column(default=False)

    chat: Mapped['Chat'] = relationship(back_populates='messages')
    sender: Mapped['User'] = relationship(back_populates='messages')
