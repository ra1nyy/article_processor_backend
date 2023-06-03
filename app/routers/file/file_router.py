from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, UploadFile, Path
from fastapi.responses import FileResponse

from app.api_utils.auth_checker import check_by_role, oauth_scheme
from app.core.containers import Container, inject_module
from app.models import UserRoleEnum, User
from app.models.file.article_form_request import FileDomain
from app.routers.custom_api_router import CustomApiRouter
from app.routers.file.docs import file_docs
from app.services.file.file_service import FileService

inject_module(__name__)

file_router = CustomApiRouter(
    prefix='/file',
    tags=[file_docs["name"]],
)


@file_router.get(
    "/{file_id}",
    response_class=FileResponse,
)
@check_by_role()
@inject
async def get_file(
    file_id: Annotated[int, Path()],
    file_service: FileService = Depends(Provide[Container.file_service]),
    current_user: User = Depends(oauth_scheme),
):
    """
    Endpoint для получения файла
    """
    return await file_service.load_document(file_id=file_id)


@file_router.get(
    "/metadata/{file_id}",
    response_model=FileDomain,
)
@check_by_role()
@inject
async def get_file_metadata(
    file_id: Annotated[int, Path()],
    file_service: FileService = Depends(Provide[Container.file_service]),
    current_user: User = Depends(oauth_scheme),
):
    """
    Endpoint для получения метадаты файла
    """
    return await file_service.load_document_metadata(file_id=file_id)


@file_router.get(
    "/metadata/",
    response_model=list[FileDomain],
)
@check_by_role([UserRoleEnum.ADMIN])
@inject
async def get_files_metadata(
    file_service: FileService = Depends(Provide[Container.file_service]),
    current_user: User = Depends(oauth_scheme),
):
    """
    Endpoint для получения метадаты всех файлов
    """
    return await file_service.get_all_entities()


@file_router.post(
    "/",
    response_model=FileDomain,
)
@check_by_role()
@inject
async def upload_document(
    file_doc: UploadFile,
    file_service: FileService = Depends(Provide[Container.file_service]),
    current_user: User = Depends(oauth_scheme),
):
    """
    Endpoint для получения токена авторизации
    """
    return await file_service.upload_document(file_doc=file_doc)
