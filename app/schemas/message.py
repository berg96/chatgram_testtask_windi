from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

from core.constants import MAX_LENGTH_MESSAGE_TEXT


class MessageBase(BaseModel):
    text: str = Field(..., max_length=MAX_LENGTH_MESSAGE_TEXT)
    chat_id: UUID
    sender_id: UUID


class MessageCreate(MessageBase):
    pass


class MessageUpdate(BaseModel):
    text: Optional[str] = Field(None, max_length=MAX_LENGTH_MESSAGE_TEXT)
    is_read: Optional[bool] = None


class MessageRead(MessageBase):
    id: UUID
    timestamp: datetime
    is_read: bool

    class Config:
        orm_mode = True
