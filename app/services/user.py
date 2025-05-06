import logging
from typing import Union, Optional
from uuid import UUID

from fastapi import Request, Response
from fastapi_users import (
    UUIDIDMixin, BaseUserManager, InvalidPasswordException
)

from core import constants
from models import User
from schemas.user import UserCreate


logger = logging.getLogger(__name__)


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

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ):
        logger.info('Зарегистрирован новый пользователь')

    async def on_after_login(
        self, user: User,
        request: Optional[Request] = None, response: Optional[Response] = None
    ):
        logger.info('Пользователь вошёл в систему')
