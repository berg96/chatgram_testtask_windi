from typing import Optional, Literal, List
from uuid import UUID
from pydantic import BaseModel, Field, model_validator

from core.constants import MAX_LENGTH_CHAT_NAME
from dependencies.database import get_async_session
from repositories.chat import chat_repo
from schemas.message import MessageRead
from schemas.user import UserRead


class GroupBase(BaseModel):
    pass


class GroupCreate(GroupBase):
    type: Optional[Literal['group',]]
    members: list[UUID]
    name: str = Field(..., max_length=MAX_LENGTH_CHAT_NAME)


class GroupUpdate(GroupBase):
    members: Optional[list[UUID]] = Field(None)
    name: Optional[str] = Field(None, max_length=MAX_LENGTH_CHAT_NAME)


class GroupRead(GroupBase):
    id: UUID
    creator_id: UUID
    chat_id: UUID
    name: str
    type: Literal['group',]
    members: List[UserRead]
    messages: List[MessageRead]

    class Config:
        from_attributes = True
