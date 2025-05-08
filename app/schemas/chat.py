from typing import Literal, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from core.constants import MAX_LENGTH_CHAT_NAME
from schemas.message import MessageRead
from schemas.user import UserRead


class ChatBase(BaseModel):
    name: str = Field(..., max_length=MAX_LENGTH_CHAT_NAME)
    type: Literal['private', 'group']

class ChatCreate(ChatBase):
    other_user_id: Optional[UUID] = None


class ChatUpdate(ChatBase):
    name: Optional[str] = Field(None, max_length=MAX_LENGTH_CHAT_NAME)
    type: Optional[Literal['private', 'group']] = None


class ChatRead(ChatBase):
    id: UUID
    members: List[UserRead]
    messages: List[MessageRead]

    class Config:
        orm_mode = True
