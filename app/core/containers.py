from typing import Set

from dependency_injector import containers, providers

from app.core.containers_uitils.article_form import get_article_form_service
from app.core.containers_uitils.auth_service import get_auth_service
from app.core.containers_uitils.base import get_database, get_di_config, get_di_logger
from app.core.containers_uitils import (
    get_user_service,
)
from app.core.containers_uitils.doc_service import get_doc_service
from app.core.containers_uitils.file_service import get_file_service

modules: Set = set()


class Container(containers.DeclarativeContainer):
    # Base
    config = get_di_config()
    logger = get_di_logger(providers, config)
    database = get_database(providers, config)

    # ---------- Services start ---------- #
    user_service = get_user_service(
        providers=providers,
        session=database.provided.session,
        config=config,
        logger=logger,
    )
    auth_service = get_auth_service(
        providers=providers,
        session=database.provided.session,
        user_service=user_service,
        config=config,
        logger=logger,
    )
    doc_service = get_doc_service(
        providers=providers,
    )
    file_service = get_file_service(
        providers=providers,
        session=database.provided.session,
        config=config,
        logger=logger,
        doc_service=doc_service,
    )
    article_form_service = get_article_form_service(
        providers=providers,
        session=database.provided.session,
        config=config,
        logger=logger,
        user_service=user_service,
        file_service=file_service,
    )
    # ---------- Services end ---------- #


container = Container()


def inject_module(module_name: str):
    modules.add(module_name)


def wire_modules():
    container.wire(modules=list(modules))
