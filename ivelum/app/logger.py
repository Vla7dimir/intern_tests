"""Logging configuration module."""

import logging
import sys
from typing import Optional

from config.settings import settings


def setup_logging(log_level: Optional[str] = None) -> None:
    """Configure application logging.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
                   If None, uses log_level from settings.
    """
    if log_level is None:
        log_level = getattr(settings, "log_level", "INFO").upper()
    log_format = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s "
        "[%(filename)s:%(lineno)d]"
    )
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True, 
    )

    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Return logger for the given module name."""
    return logging.getLogger(name)
