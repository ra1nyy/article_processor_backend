from app.core.config import get_config
from app.core.logger.appLogger import AppLogger
from app.database.db import AsyncDb


def get_di_config():
    return get_config()


def get_di_logger(providers, config):
    return providers.Singleton(
        AppLogger,
        level=config.logger_level,
        developer_logger=config.developer_logger,
        gl_host=config.graylog_host,
        gl_port=config.graylog_port,
        gl_facility=config.graylog_facility,
    )


def get_database(providers, config):
    return providers.Singleton(
        AsyncDb,
        db_url=config.db_url,
        debug=config.debug,
    )
