from typing import Union
from uuid import UUID

from fastapi_users import (
    UUIDIDMixin, BaseUserManager, InvalidPasswordException
)

from core import constants
from db import User
from schemas.user import UserCreate


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        if len(password) < constants.MIN_LENGTH_USER_PASSWORD:
            raise InvalidPasswordException(
                reason=constants.INVALID_PASS_MIN_LEN
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason=constants.INVALID_PASS_CONSIST_EMAIL
            )

    # async def on_after_register(
    #     self, user: User, request: Optional[Request] = None
    # ):
    #     # Вместо print здесь можно было бы настроить отправку письма.
    #     print(f'Пользователь {user.email} зарегистрирован.')
