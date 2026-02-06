"""FastAPI application for AB Testing API.

This module provides REST API endpoints for AB testing experiments.
Business logic is separated into manager layer (app.experiments.manager).
"""

from contextlib import asynccontextmanager
from pathlib import Path
from typing import List

from fastapi import Depends, FastAPI, Header, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.db.migrations import run_migrations
from app.experiments.manager import ExperimentManager
from app.logger import get_logger, setup_logging
from app.schemas.experiment import ExperimentResponse, StatisticsResponse

setup_logging()
logger = get_logger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "templates"
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


@asynccontextmanager
async def lifespan(app: FastAPI):
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


@app.get(
    "/api/v1/experiments",
    response_model=ExperimentResponse,
    tags=["Experiments"],
    summary="Get experiments for device",
    description=(
        "Get assigned experiment values for a device. "
        "If device is new, assigns experiments based on weights. "
        "If device already exists, returns previously assigned values."
    ),
    responses={
        200: {
            "description": "Experiments assigned successfully",
            "content": {
                "application/json": {
                    "example": {
                        "button_color": "#FF0000",
                        "price": "10",
                    }
                }
            },
        },
        422: {"description": "Device-Token header is missing"},
        500: {"description": "Internal server error"},
    },
)
async def get_experiments(
    device_token: str = Header(..., alias="Device-Token"),
    db: Session = Depends(get_db),
) -> ExperimentResponse:
    """Get experiments for device.

    Args:
        device_token: Device token from Device-Token header.
        db: Database session.

    Returns:
        ExperimentResponse with assigned experiment values.

    Raises:
        HTTPException: If device token is missing (422) or operation fails (500).
    """
    logger.info("Getting experiments for device", extra={"device_token": device_token})
    try:
        manager = ExperimentManager(db)
        experiments = manager.get_experiments_for_device(device_token)
        logger.info(
            "Experiments retrieved",
            extra={
                "device_token": device_token,
                "experiments": list(experiments.keys()),
            },
        )
        return ExperimentResponse(**experiments)
    except Exception as e:
        logger.error(
            "Failed to get experiments",
            extra={"device_token": device_token, "error": str(e)},
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get experiments",
        ) from e


@app.get(
    "/api/v1/statistics",
    response_model=List[StatisticsResponse],
    tags=["Statistics"],
    summary="Get experiment statistics",
    description=(
        "Get statistics for all experiments including distribution "
        "of devices across experiment options with counts, weights, and percentages."
    ),
    responses={
        200: {
            "description": "Statistics retrieved successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "experiment_key": "button_color",
                            "total_devices": 100,
                            "distribution": {
                                "#FF0000": {
                                    "count": 33,
                                    "weight": 33,
                                    "percentage": 33.0,
                                },
                            },
                        },
                    ]
                }
            },
        },
        500: {"description": "Internal server error"},
    },
)
async def get_statistics(
    db: Session = Depends(get_db),
) -> List[StatisticsResponse]:
    """Get experiment statistics.

    Args:
        db: Database session.

    Returns:
        List of StatisticsResponse with experiment statistics.

    Raises:
        HTTPException: If operation fails (500).
    """
    logger.info("Getting statistics")
    try:
        manager = ExperimentManager(db)
        stats = manager.get_statistics()
        logger.info("Statistics retrieved", extra={"experiments_count": len(stats)})
        return [StatisticsResponse(**stat) for stat in stats]
    except Exception as e:
        logger.error("Failed to get statistics", extra={"error": str(e)}, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get statistics",
        ) from e


@app.get(
    "/statistics",
    response_class=HTMLResponse,
    tags=["Statistics"],
    summary="Statistics HTML page",
    description="Get experiment statistics as HTML page",
    responses={
        200: {
            "description": "Statistics page rendered successfully",
            "content": {"text/html": {}},
        },
        500: {"description": "Internal server error"},
    },
)
async def statistics_page(
    request: Request,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    """Get statistics as HTML page.

    Args:
        request: FastAPI request object.
        db: Database session.

    Returns:
        HTMLResponse with rendered statistics page.

    Raises:
        HTTPException: If operation fails (500).
    """
    logger.info("Getting statistics page")
    try:
        manager = ExperimentManager(db)
        stats = manager.get_statistics()
        logger.info("Statistics page rendered", extra={"experiments_count": len(stats)})
        return templates.TemplateResponse(
            "statistics.html",
            {"request": request, "statistics": stats},
        )
    except Exception as e:
        logger.error("Failed to render statistics page", extra={"error": str(e)}, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to render statistics page",
        ) from e
