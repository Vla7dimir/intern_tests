"""Logging configuration module."""

import logging
import sys
from typing import Optional

from config.settings import settings


def setup_logging(log_level: Optional[str] = None) -> None:
    """Configure application logging.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
                   If None, uses LOG_LEVEL from settings or defaults to INFO.
    """
    if log_level is None:
        log_level = getattr(settings, "log_level", "INFO").upper()

    log_format = (
        "%(asctime)s - %(name)s - %(levelname)s - "
        "%(message)s - [%(filename)s:%(lineno)d]"
    )

    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )

    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("alembic").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get logger instance for a module.

    Args:
        name: Logger name (usually __name__).

    Returns:
        Configured logger instance.
    """
    return logging.getLogger(name)
