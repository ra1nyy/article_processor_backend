import sys
from logging import StreamHandler

from app.core.logger.models.loggerExtra import LoggerExtra
from app.core.logger.utils.jsonFormatter import JsonFormatter

fields_json_ordering = {
    "level": "levelname",
    "message": "message",
    "timestamp": "asctime",
    **LoggerExtra.get_extra_fields(),
    "processName": "processName",
    "processID": "process",
    "threadName": "threadName",
    "threadID": "thread",
}

JsonHandler = StreamHandler(sys.stdout)
json_formatter = JsonFormatter(fields_json_ordering)
JsonHandler.setFormatter(json_formatter)
