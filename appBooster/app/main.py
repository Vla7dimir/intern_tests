"""FastAPI application entry point.

Creates and configures the FastAPI application.
API routes are defined in app.api module.
"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from app.api.pages import router as pages_router
from app.api.v1 import api_router
from app.db.migrations import run_migrations
from app.logger import get_logger, setup_logging

setup_logging()
logger = get_logger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Application lifespan manager.

    Runs migrations on startup (Alembic or create_all fallback).

    Yields:
        None: Application is ready to serve requests.
    """
    logger.info("Starting application")
    try:
        run_migrations()
        logger.info("Application startup complete")
    except Exception as e:
        logger.error("Failed to start application", extra={"error": str(e)}, exc_info=True)
        raise
    yield
    logger.info("Application shutdown")


app = FastAPI(
    title="AB Testing API",
    version="1.0.0",
    description="REST API for AB testing experiments with device assignment and statistics",
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

app.include_router(api_router)
app.include_router(pages_router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests."""
    logger.info(
        "Incoming request",
        extra={
            "method": request.method,
            "path": request.url.path,
            "client": request.client.host if request.client else None,
        },
    )
    try:
        response = await call_next(request)
        logger.info(
            "Request completed",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
            },
        )
        return response
    except Exception as e:
        logger.error(
            "Request failed",
            extra={
                "method": request.method,
                "path": request.url.path,
                "error": str(e),
            },
            exc_info=True,
        )
        raise
