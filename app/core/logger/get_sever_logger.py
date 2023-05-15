import logging
import sys
import warnings

import loguru

from app.core.config import Config
from app.core.get_logger import get_logger
from app.core.logger.handlers.loguruHandler import loguru_format

app_logger = get_logger()
logger = loguru.logger

config = Config.load_config()
is_developer_mode = config.developer_mode


def get_server_logger():
    # hiding sqlalchemy hints
    if not is_developer_mode and not sys.warnoptions:
        warnings.simplefilter("ignore")

    logger.remove()
    logger.add(
        sys.stdout,
        enqueue=True,
        backtrace=True,
        level="INFO",
        format=loguru_format,
    )

    for name in logging.root.manager.loggerDict:
        logging.getLogger(name).handlers = []

    logging.getLogger("fastapi").handlers = []
    logging.getLogger("uvicorn").handlers = [*app_logger.handlers]  # noqa: WPS356
    logging.getLogger("uvicorn.access").handlers = [
        *app_logger.handlers
    ]  # noqa: WPS356
    logging.getLogger("uvicorn.errors").handlers = [
        *app_logger.handlers
    ]  # noqa: WPS356

    return logger.bind(request_id=None, method=None)
