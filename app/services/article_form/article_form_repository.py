from sqlalchemy import select

from app.database.base_repository import BaseRepository
from app.database.entities import ArticleFormEntity, ArticleAutorEntity
from app.models import User
from app.models.article_form.article_form_request import ArticleFormDomain, ArticleFormCreate


class ArticleFormRepository(BaseRepository[ArticleFormDomain]):
    model = ArticleFormDomain
    entity = ArticleFormEntity

    async def create_article(
        self,
        article_model: ArticleFormCreate,
        authors: list[User]
    ):
        async with self.db_session() as session:
            article = await self.create(article_model)

            article_authors = []
            for author in authors:
                article_authors.append(
                    ArticleAutorEntity(user_id=author.id, article_id=article.id)
                )
            session.add_all(article_authors)
            await session.commit()

            return article

    async def get_articles_by_user_id(self, user_id: int):
        async with self.db_session() as session:
            query = select(self.entity).join(ArticleAutorEntity).where(ArticleAutorEntity.user_id == user_id)
            result = await session.execute(query)
            return self.get_list(result.scalars())
