from app.models.mode_base import ModelBase


class ArticleFormBase(ModelBase):
    """Base model for Article."""

    scientific_adviser_fullname: str = None
    scientific_adviser_academic_degree: str = None
    scientific_adviser_academic_title: str = None
    scientific_adviser_institute: str = None
    scientific_adviser_department: str = None

    attached_article_text: str | None = None
    attached_docs_id: int | None = None

    list_of_references: str | None = None

    keywords_rus: str | None = None
    keywords_eng: str | None = None

    abstract_rus: str | None = None
    abstract_eng: str | None = None

    title_rus: str | None = None
    title_eng: str | None = None

    udc: str | None = None

    # @validator('attached_docs_filename')
    # def validate_attached_docs(cls, value, values: dict):
    #     print(values)
    #     print(value)
    #     if values.get('attached_docs_filename') and values.get('attached_article_text'):
    #         raise WrongDataError(message='Should be only file or text, not together')
    #     return value
