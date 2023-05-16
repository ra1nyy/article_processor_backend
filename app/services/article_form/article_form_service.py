from app.api.errors import EntityNotFound
from app.core.config import Config
from app.core.logger.appLogger import AppLogger
from app.models.article_form.article_form_request import ArticleFormDomain, ArticleFormCreate
from app.services import UserService
from app.services.article_form.article_form_repository import ArticleFormRepository
from app.services.base_service import BaseService


class ArticleFormService(BaseService[ArticleFormDomain]):
    model = ArticleFormDomain
    repository: ArticleFormRepository

    def __init__(
        self,
        repository: ArticleFormRepository,
        user_service: UserService,
        config: Config | None = None,
        logger: AppLogger | None = None,
    ) -> None:  # noqa
        super().__init__(repository, config=config, logger=logger)
        self.user_service = user_service

    @BaseService.catch_db_error(entity=ArticleFormDomain.__name__, unique_field="symbol")
    async def create_entity(self, article_to_create: ArticleFormCreate) -> ArticleFormDomain:
        authors = await self.user_service.get_users_by_list_ids(
            article_to_create.authors_ids,
        )

        if not authors:
            raise EntityNotFound('User')

        article_to_response = await self.repository.create_article(
            article_model=article_to_create,
            authors=authors,
        )
        article_to_response.authors = authors
        return article_to_response
