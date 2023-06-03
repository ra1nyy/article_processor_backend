from datetime import datetime
from typing import Optional

from pydantic.fields import Field

from app.models import User
from app.models.article_form.article_form import ArticleFormBase
from app.models.mode_base import UpdateBase


class ArticleFormDomain(ArticleFormBase):
    id: int = None
    authors: Optional[list[User]] = None
    formatted_docs_id: int | None = None

    created_at: datetime | None = Field(
        default=datetime.utcnow(),
        description="Дата создания операции",
    )
    updated_at: datetime = None


class ArticleFormResponse(ArticleFormDomain):
    formatted_docs_id: int | None = None


class ArticleFormCreate(ArticleFormBase):
    authors_ids: list[int] = None


class ArticleFormUpdate(UpdateBase, ArticleFormBase):
    ...
