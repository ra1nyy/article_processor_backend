from fastapi import APIRouter, FastAPI

from app.core.config import get_config
from app.core.containers import inject_module
from app.routers import (
    user_router,
    auth_router,
)

inject_module(__name__)

router = APIRouter(
    tags=["article-backend"],
)

config = get_config()


def add_routers(app: FastAPI):
    routers = [
        user_router,
        auth_router,
    ]
    _add_routers(app, routers)


def _add_routers(app: FastAPI, routers: list[APIRouter]):
    for rout in routers:
        app.include_router(rout)
