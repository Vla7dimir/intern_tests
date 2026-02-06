"""Run Alembic migrations on startup."""

import os
from pathlib import Path

from alembic import command
from alembic.config import Config
from alembic.util.exc import CommandError

from config.settings import settings
from app.db.connection import Base, engine
from app.logger import get_logger

logger = get_logger(__name__)


def run_migrations() -> None:
    """Run database migrations on startup.

    Tries to run Alembic migrations first, falls back to create_all if Alembic fails.
    """
    base_dir = Path(__file__).resolve().parent.parent.parent.parent
    alembic_ini_path = base_dir / "migrations" / "alembic.ini"
    alembic_cfg = Config(str(alembic_ini_path))
    alembic_cfg.set_main_option("sqlalchemy.url", settings.database_url)
    try:
        logger.info("Running Alembic migrations")
        command.upgrade(alembic_cfg, "head")
        logger.info("Alembic migrations completed successfully")
    except (CommandError, FileNotFoundError) as e:
        logger.warning(
            "Alembic migration failed, falling back to create_all",
            extra={"error": str(e)},
        )
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables created using create_all")
        except Exception as create_error:
            logger.error(
                "Failed to create database tables",
                extra={"error": str(create_error)},
                exc_info=True,
            )
            raise
