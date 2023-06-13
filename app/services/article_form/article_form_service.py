import uuid

from app.core.config import Config
from app.core.logger.appLogger import AppLogger
from app.models import User
from app.models.article_form.article_form_request import ArticleFormDomain, ArticleFormCreate, ArticleFormResponse
from app.services import UserService
from app.services.article_form.article_form_repository import ArticleFormRepository
from app.services.base_service import BaseService
from app.services.file.file_service import FileService


class ArticleFormService(BaseService[ArticleFormDomain]):
    model = ArticleFormDomain
    repository: ArticleFormRepository

    def __init__(
        self,
        repository: ArticleFormRepository,
        user_service: UserService,
        file_service: FileService,
        config: Config | None = None,
        logger: AppLogger | None = None,
    ) -> None:  # noqa
        super().__init__(repository, config=config, logger=logger)
        self.user_service = user_service
        self.file_service = file_service

    @BaseService.catch_db_error(entity=ArticleFormDomain.__name__)
    async def create_entity(
        self,
        article_to_create: ArticleFormCreate,
        user: User,
    ) -> ArticleFormDomain:
        authors = await self.user_service.get_users_by_list_ids(
            article_to_create.authors_ids,
        )

        article_to_response = await self.repository.create_article(
            article_model=article_to_create,
            authors=authors,
        )

        article_to_response.authors = authors

        formatted_docx = await self.file_service.create_formatted_docx(
            article_to_response,
            attached_text=article_to_create.attached_article_text,
            filename=f'{user.last_name}_Статья_{uuid.uuid4()}.doc',
        )
        article_to_response.formatted_docs_id = formatted_docx.id
        await self.repository.update(article_to_response)

        return ArticleFormResponse(
            **article_to_response.dict(exclude={'formatted_docs_id'}),
            formatted_docs_id=formatted_docx.id,
        )

    async def get_all_entities_by_user_id(self, user_id: int):
        return await self.repository.get_articles_by_user_id(user_id=user_id)
