from app.services.article_form.article_form_repository import ArticleFormRepository
from app.services.article_form.article_form_service import ArticleFormService


def get_article_form_service(
    providers,
    session,
    config,
    logger,
    user_service,
    file_service,
):
    article_form_repository = providers.Factory(
        ArticleFormRepository,
        db_session=session,
    )

    return providers.Factory(
        ArticleFormService,
        config=config,
        repository=article_form_repository,
        logger=logger,
        user_service=user_service,
        file_service=file_service,
    )
