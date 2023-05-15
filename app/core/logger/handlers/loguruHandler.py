import logging

import loguru

loguru_format = "<level>{level: <8}</level> <green>{time:YYYY-MM-DD HH:mm:ss}</green> - <level>{message}</level>"
loguru_logger = loguru.logger


class LoguruHandler(logging.Handler):
    def emit(self, record):
        try:
            level = loguru_logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        loguru_logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )
