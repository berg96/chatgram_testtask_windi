from typing import Optional
from uuid import UUID

from fastapi_users import schemas
from pydantic import Field

from core.constants import MIN_LENGTH_USER_NAME, MAX_LENGTH_USER_NAME


class UserCreate(schemas.BaseUserCreate):
    name: str = Field(
        ..., min_length=MIN_LENGTH_USER_NAME, max_length=MAX_LENGTH_USER_NAME
    )


class UserUpdate(schemas.BaseUserUpdate):
    name: Optional[str] = None


class UserRead(schemas.BaseUser[UUID]):
    name: str
