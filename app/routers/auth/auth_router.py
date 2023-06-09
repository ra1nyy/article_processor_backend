from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from app.api.doc_response_error import doc_response_errors
from app.api.errors import ApiAccessError, ApiPermissionError, UniqueError
from app.api_utils.auth_checker import check_by_role, oauth_scheme
from app.core.containers import Container, inject_module
from app.models import Token, User
from app.models.auth.refresh_token import RefreshToken
from app.models.user.user_requests import UserRegisterRequest
from app.routers.auth.docs import auth_docs
from app.routers.custom_api_router import CustomApiRouter
from app.services.auth.auth_service import AuthService

inject_module(__name__)

auth_router = CustomApiRouter(
    tags=[auth_docs["name"]],
)


@auth_router.post(
    "/login",
    response_model=Token,
)
@inject
async def auth(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    """
    Endpoint для получения токена авторизации
    """
    return await auth_service.login(
        form_data.username,
        form_data.password,
    )


@auth_router.post(
    "/refresh-token",
    response_model=Token,
)
@inject
async def refresh_token(
    form_data: RefreshToken,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    """
    Endpoint для обновления истекшего токена.
    Необходимый тут refresh-токен поставляется в ответе на получение первичного токена
    """
    return await auth_service.refresh_token(form_data.refresh_token)


@auth_router.get(
    "/logout",
    responses=doc_response_errors(
        ApiAccessError(),
        ApiPermissionError(),
    ),
)
@check_by_role()
@inject
async def logout(
    current_token: str = Depends(oauth_scheme),
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    """
    Принудительно устанавливает текущий токен истекшим
    """
    await auth_service.logout(current_token)


@auth_router.post(
    "/register",
    response_model=User,
    responses=doc_response_errors(
        ApiAccessError(),
        ApiPermissionError(),
        UniqueError('Email not unique !'),
    ),
)
@inject
async def registration(
    user_creds: UserRegisterRequest,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    """
    Принудительно устанавливает текущий токен истекшим
    """
    return await auth_service.register(user_creds)
