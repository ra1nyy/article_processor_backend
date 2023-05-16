from typing import Annotated
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Request, Path

from app.core.containers import Container, inject_module
from app.models.article_form.article_form_request import ArticleFormDomain, ArticleFormCreate
from app.routers.article_form.docs import article_docs
from app.routers.custom_api_router import CustomApiRouter
from app.services.article_form.article_form_service import ArticleFormService

inject_module(__name__)

article_form_router = CustomApiRouter(
    prefix='/article',
    tags=[article_docs["name"]],
)


@article_form_router.get(
    "/{article_form_id}",
    response_model=ArticleFormDomain,
)
@inject
async def get_article(
    article_form_id: Annotated[int, Path()],
    article_form_service: ArticleFormService = Depends(Provide[Container.article_form_service]),
):
    """
    Endpoint для получения токена авторизации
    """
    return await article_form_service.get_entity_by_id(article_form_id)


@article_form_router.post(
    "/",
    response_model=ArticleFormDomain,
)
@inject
async def create_article(
    article_form_create: ArticleFormCreate,
    article_form_service: ArticleFormService = Depends(Provide[Container.article_form_service]),
):
    """
    Endpoint для получения токена авторизации
    """
    return await article_form_service.create_entity(
        article_to_create=article_form_create,
    )
