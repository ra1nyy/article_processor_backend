from app.core.config import get_config
from app.core.logger.appLogger import AppLogger

config = get_config()

logger = AppLogger(
    level=config.logger_level,
    gl_host=config.graylog_host,
    gl_port=config.graylog_port,
    gl_facility=config.graylog_facility,
    developer_logger=config.developer_logger,
)


def get_logger():
    return logger
