from typing import Optional

from app.models import User
from app.models.article_form.article_form import ArticleFormBase
from app.models.mode_base import UpdateBase


class ArticleFormDomain(ArticleFormBase):
    id: int = None
    authors: Optional[list[User]] = None


class ArticleFormCreate(ArticleFormBase):
    authors_ids: list[int] = None


class ArticleFormUpdate(UpdateBase, ArticleFormBase):
    ...
