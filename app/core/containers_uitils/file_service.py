from app.services.file.file_repository import FileRepository
from app.services.file.file_service import FileService


def get_file_service(providers, session, config, logger, doc_service):
    file_repository = providers.Factory(
        FileRepository,
        db_session=session,
    )

    return providers.Factory(
        FileService,
        config=config,
        repository=file_repository,
        logger=logger,
        doc_service=doc_service,
    )
