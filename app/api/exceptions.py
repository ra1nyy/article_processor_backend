from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.core.get_logger import get_logger

logger = get_logger()


def add_exceptions(app: FastAPI):
    @app.exception_handler(ValidationError)
    async def validation_exception_handler(  # noqa: WPS430
        request: Request,
        exc: ValidationError,
    ):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"detail": exc.errors()}),
        )

    @app.exception_handler(Exception)
    async def exception_logger_handler(  # noqa: WPS430, F811
        request: Request,
        exc: Exception,
    ):
        logger.exception(exc)
        raise exc
