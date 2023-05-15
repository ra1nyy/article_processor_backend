from fastapi import FastAPI

from app.api.docs import docs_tags
from app.api.docs_router import docs_router
from app.api.exceptions import add_exceptions
from app.api.routers import add_routers
from app.core.config import get_config
from app.core.logger.get_sever_logger import get_server_logger


def create_api_server() -> FastAPI:
    config = get_config()

    app = FastAPI(
        openapi_tags=docs_tags,
        docs_url=None,
        redoc_url=None,
        root_path=config.root_path,
    )

    app.logger = get_server_logger()

    add_exceptions(app)
    add_routers(app)
    docs_router(app)

    return app
