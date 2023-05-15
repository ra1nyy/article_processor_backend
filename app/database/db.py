from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool


class AsyncDb(object):
    def __init__(self, db_url: str, debug: bool):
        engine = create_async_engine(
            db_url,
            echo=debug,
            poolclass=NullPool,
        )

        self.session = sessionmaker(
            engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )
