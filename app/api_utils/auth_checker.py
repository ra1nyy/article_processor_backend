from functools import wraps
from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi.security import OAuth2PasswordBearer

from app.api.errors import ApiAccessError, ApiPermissionError
from app.core.config import get_config
from app.core.containers import Container, inject_module
from app.models import User, UserRoleEnum, UserSession
from app.services.auth.auth_service import AuthService

config = get_config()
oauth_scheme = OAuth2PasswordBearer(tokenUrl=f"{config.root_path}/login")
inject_module(__name__)


def check_by_role(roles: List[UserRoleEnum] = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(
            *args,
            **kwargs,
        ):
            token_key = _get_token(**kwargs)

            session = await _get_session(token_key)
            if not session:
                raise ApiAccessError()

            user = await _get_user(session)
            _validate_user(user, roles=roles)

            if "current_user" in kwargs:
                kwargs["current_user"] = user

            return await func(*args, **kwargs)

        return wrapper

    return decorator


@inject
async def _get_session(
    token_key: str,
    auth_service: AuthService = Provide[Container.auth_service],
) -> UserSession:
    return await auth_service.get_user_session(token_key)


@inject
async def _get_user(
    session: UserSession,
    auth_service: AuthService = Provide[Container.auth_service],
) -> User:
    return await auth_service.get_user_by_session(session)


def _validate_user(user: User | None, roles: List[UserRoleEnum] = None):
    if not user:
        raise ApiAccessError()

    if user.role == UserRoleEnum.ADMIN:
        return
    if roles is not None:
        if user.role not in [role.value for role in roles]:
            raise ApiPermissionError()


def _get_token(**kwargs) -> str:
    token = kwargs.get("current_user") or kwargs.get("current_token")

    if not token:
        raise ApiAccessError()

    return token
