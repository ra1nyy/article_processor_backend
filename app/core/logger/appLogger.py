import logging
import sys
import graypy as graypy

from app.core.logger.handlers.jsonHandler import JsonHandler
from app.core.logger.handlers.loguruHandler import (
    LoguruHandler,
    loguru_format,
    loguru_logger,
)
from app.core.logger.utils.get_dicts_difference import get_dicts_difference


class AppLogger(logging.Logger):
    def __init__(
        self,
        level: str = "NOTSET",
        gl_host: str = None,
        gl_port: int = None,
        gl_facility: str = None,
        developer_logger: bool | None = None,
    ):
        level = level.upper()
        super().__init__(__name__, level)

        if None not in [gl_host, gl_port, gl_facility]:
            g_handler = graypy.GELFUDPHandler(
                host=gl_host,
                port=gl_port,
                facility=gl_facility,
                extra_fields=True,
                level_names=level,
            )
            self.addHandler(g_handler)

        if not developer_logger:
            self.addHandler(JsonHandler)
        else:
            loguru_logger.remove()
            loguru_logger.add(sys.stdout, format=loguru_format, level=level)

            self.addHandler(LoguruHandler())

    def _update_difference_to_model_changes(
        self, extra: dict, previous: dict, updated: dict
    ):
        dict_diff = get_dicts_difference(previous, updated)
        for field, updated_value in dict_diff:
            previous_key = self._create_previous_key(field)
            extra[previous_key] = previous[field]

            update_key = self._create_updated_key(field)
            extra[update_key] = updated_value

    @classmethod
    def _create_previous_key(cls, field_key: str):
        return "".join(["change_", field_key, "_taken_off"])

    @classmethod
    def _create_updated_key(cls, field_key: str):
        return "".join(["change_", field_key, "_updated"])
