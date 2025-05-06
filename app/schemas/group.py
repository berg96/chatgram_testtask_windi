from uuid import UUID
from pydantic import BaseModel, Field

from schemas.chat import ChatRead


class GroupBase(BaseModel):
    pass


class GroupCreate(GroupBase):
    creator_id: UUID


class GroupUpdate(GroupBase):
    pass


class GroupRead(ChatRead):
    creator_id: UUID

    class Config:
        orm_mode = True
