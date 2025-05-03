from fastapi_users.authentication import (
    AuthenticationBackend, BearerTransport, JWTStrategy
)

from core.config import settings
from core.constants import JWT_LIFETIME_SECONDS


bearer_transport = BearerTransport(tokenUrl='api/auth/login')


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.secret, lifetime_seconds=JWT_LIFETIME_SECONDS
    )


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
