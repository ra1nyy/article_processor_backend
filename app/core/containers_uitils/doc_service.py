from app.services.doc_service.doc_service import DocService


def get_doc_service(providers):

    return providers.Factory(
        DocService,
    )
