from typing import Set

from dependency_injector import containers, providers

from app.core.containers_uitils.auth_service import get_auth_service
from app.core.containers_uitils.base import get_database, get_di_config, get_di_logger
from app.core.containers_uitils import (
    get_user_service,
)

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
    # ---------- Services end ---------- #


container = Container()


def inject_module(module_name: str):
    modules.add(module_name)


def wire_modules():
    container.wire(modules=list(modules))
