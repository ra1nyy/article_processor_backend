import sqlalchemy as sa

from app.database.base import Base
from app.database.entity_base import EntityBase


class ArticleAutorEntity(Base, EntityBase[...]):
    __tablename__ = "article_autor"
    model = ...

    id = sa.Column(sa.INTEGER, sa.Identity(), primary_key=True, nullable=False)

    user_id = sa.Column(
        sa.INTEGER,
        sa.ForeignKey("user.id", onupdate="RESTRICT", ondelete="RESTRICT"),
        nullable=False,
    )
    article_id = sa.Column(
        sa.INTEGER,
        sa.ForeignKey("article_form.id", onupdate="RESTRICT", ondelete="RESTRICT"),
        nullable=False,
    )
