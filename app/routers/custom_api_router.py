from fastapi import APIRouter

from app.core.config import get_config


class CustomApiRouter(APIRouter):
    config = get_config()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = self._get_abs_prefix(kwargs.get('prefix'))

    def _get_abs_prefix(self, prefix: str):
        return self.config.routers_root_path + (prefix if prefix else '')
