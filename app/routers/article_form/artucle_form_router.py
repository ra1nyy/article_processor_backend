from typing import Annotated
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Path

from app.api_utils.auth_checker import check_by_role, oauth_scheme
from app.core.containers import Container, inject_module
from app.models import User
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
@check_by_role()
@inject
async def get_article(
    article_form_id: Annotated[int, Path()],
    article_form_service: ArticleFormService = Depends(Provide[Container.article_form_service]),
    current_user: User = Depends(oauth_scheme),
):
    """
    Endpoint для получения статьи
    """
    return await article_form_service.get_entity_by_id(article_form_id)


@article_form_router.get(
    "",
    response_model=list[ArticleFormDomain],
)
@check_by_role()
@inject
async def get_articles(
    article_form_service: ArticleFormService = Depends(Provide[Container.article_form_service]),
    current_user: User = Depends(oauth_scheme),
):
    """
    Endpoint для получения всех статей
    """
    return await article_form_service.get_all_entities()


@article_form_router.post(
    "",
    response_model=ArticleFormDomain,
)
@check_by_role()
@inject
async def create_article(
    article_form_create: ArticleFormCreate,
    article_form_service: ArticleFormService = Depends(Provide[Container.article_form_service]),
    current_user: User = Depends(oauth_scheme),
):
    """
    Endpoint для создания статьи
    """
    return await article_form_service.create_entity(
        article_to_create=article_form_create,
    )
