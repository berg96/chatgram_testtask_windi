from typing import Literal, List, Optional
from uuid import UUID

from pydantic import BaseModel

from schemas.message import MessageRead
from schemas.user import UserRead


class ChatBase(BaseModel):
    type: Optional[Literal['private',]]


class ChatCreate(ChatBase):
    other_user_id: UUID


class ChatUpdate(ChatBase):
    pass


class ChatRead(ChatBase):
    id: UUID
    name: str
    members: List[UserRead]
    messages: List[MessageRead]

    class Config:
        from_attributes = True
