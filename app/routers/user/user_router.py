from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from app.api.doc_response_error import doc_response_errors
from app.api.errors import (
    ApiAccessError,
    ApiPermissionError,
    EntityNotFound,
    EntityCreateError,
)
from app.api_utils.auth_checker import check_by_role, oauth_scheme
from app.core.containers import Container, inject_module
from app.models import User
from app.models.user.user_requests import UserUpdate
from app.models.user.user_response import UserResponse
from app.routers.custom_api_router import CustomApiRouter
from app.routers.user.docs import user_docs
from app.services import UserService

inject_module(__name__)

user_router = CustomApiRouter(
    tags=[user_docs["name"]],
    prefix="/user"
)


@user_router.get(
    "/profile",
    response_model=User,
)
@check_by_role()
@inject
async def get_profile(
    current_user: User = Depends(oauth_scheme),
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    """
    Возвращает все данные о пользователе за исключением хеша пароля.
    """
    return await user_service.get_by_username(current_user.username)


@user_router.put(
    "/profile",
    response_model=UserResponse,
    responses=doc_response_errors(
        EntityNotFound("User"),
        ApiAccessError(),
        ApiPermissionError(),
        EntityCreateError(entity=User.__name__),
    ),
)
@check_by_role()
@inject
async def update_profile(
    profile_update: UserUpdate,
    current_user: User = Depends(oauth_scheme),
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    """
    Обновление данных о пользователе.
    """
    return await user_service.update_user(
        profile_update,
        current_user.id,
        current_user.role,  # type: ignore
    )
