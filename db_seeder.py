"""Seeder for mock data in DB."""
from app.core.get_logger import get_logger
from development_utils.seeding.seed_db import seed_db
from development_utils.seeding.utils.db_utils import restart_index
from development_utils.utils.get_engine import (
    get_dev_engine,
    get_session_from_engine_connect,
)
from sqlalchemy import inspect

logger = get_logger()

if __name__ == "__main__":
    engine = get_dev_engine()
    tables: list[str] = []
    inspector = inspect(engine)
    for table_name in inspector.get_table_names(schema="public"):
        tables.append(table_name)
    with engine.connect() as sql_engine:
        session = get_session_from_engine_connect(sql_engine)
        seed_db(session, logger)
        restart_index(engine=engine)
