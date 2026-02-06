"""FastAPI application for URL Shortener service."""

from typing import Dict

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import settings
from app.database import Base, engine, get_session
from app.exceptions import CodeAlreadyExistsError, CodeNotFoundError
from app.logger import get_logger, setup_logging
from app.repository import get_by_code, save_url
from app.schemas import CreateRequest, CreateResponse

setup_logging()
logger = get_logger(__name__)

app = FastAPI(
    title="URL Shortener",
    version="1.0.0",
    description="HTTP сервис для сокращения URL с поддержкой кастомных ссылок",
)


@app.on_event("startup")
def init_db() -> None:
    """Initialize database tables on startup."""
    logger.info("Initializing database tables")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully")
    except Exception as e:
        logger.error("Failed to initialize database tables", exc_info=True)
        raise


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


@app.post(
    "/api/v1/shorten",
    response_model=CreateResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["URL Management"],
    summary="Create shortened URL",
    description=(
        "Создает короткую ссылку для указанного URL. "
        "Можно указать кастомный код или использовать автогенерированный."
    ),
    responses={
        201: {
            "description": "URL успешно сокращен",
            "content": {
                "application/json": {
                    "example": {
                        "short": "http://localhost:8000/abc123",
                        "original": "https://www.example.com",
                        "code": "abc123",
                    }
                }
            },
        },
        400: {"description": "Неверный формат URL или кода"},
        409: {"description": "Код уже существует"},
    },
)
def shorten(
    request: CreateRequest,
    db: Session = Depends(get_session),
) -> CreateResponse:
    """Create shortened URL.

    Args:
        request: CreateRequest with URL and optional code.
        db: Database session.

    Returns:
        CreateResponse with shortened URL information.

    Raises:
        HTTPException: If code already exists (409).
    """
    logger.info(
        "Creating short URL",
        extra={
            "url": request.url,
            "has_custom_code": request.code is not None,
        },
    )
    try:
        record = save_url(db, request.url, request.code)
        logger.info(
            "Short URL created successfully",
            extra={
                "code": record.code,
                "original_url": record.full_url,
            },
        )
    except CodeAlreadyExistsError as e:
        logger.warning(
            "Failed to create short URL: code already exists",
            extra={"code": request.code},
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error(
            "Failed to create short URL",
            extra={"url": request.url, "error": str(e)},
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e

    return CreateResponse(
        short=f"{settings.base_url}/{record.code}",
        original=record.full_url,
        code=record.code,
    )


@app.get(
    "/{code}",
    tags=["Redirect"],
    summary="Redirect to original URL",
    description="Выполняет редирект на оригинальный URL по короткому коду",
    responses={
        302: {"description": "Редирект на оригинальный URL"},
        404: {"description": "Код не найден"},
    },
)
def redirect(
    code: str,
    db: Session = Depends(get_session),
) -> RedirectResponse:
    """Redirect to original URL by short code.

    Args:
        code: Short code to lookup.
        db: Database session.

    Returns:
        RedirectResponse to original URL.

    Raises:
        HTTPException: If code not found (404).
    """
    logger.info("Redirect request", extra={"code": code})
    try:
        record = get_by_code(db, code)
        logger.info(
            "Redirecting to original URL",
            extra={
                "code": code,
                "original_url": record.full_url,
            },
        )
    except CodeNotFoundError as e:
        logger.warning("Code not found for redirect", extra={"code": code})
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error(
            "Failed to redirect",
            extra={"code": code, "error": str(e)},
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e

    return RedirectResponse(
        url=record.full_url,
        status_code=status.HTTP_302_FOUND,
    )


@app.get(
    "/api/v1/health",
    tags=["Health"],
    summary="Health check",
    description="Проверка работоспособности сервиса",
    responses={
        200: {
            "description": "Сервис работает",
            "content": {
                "application/json": {
                    "example": {"status": "ok", "database": "connected"}
                }
            },
        },
        503: {
            "description": "Сервис недоступен",
            "content": {
                "application/json": {
                    "example": {"status": "error", "database": "disconnected"}
                }
            },
        },
    },
)
def health(db: Session = Depends(get_session)) -> Dict[str, str]:
    """Health check endpoint with database connectivity check.

    Args:
        db: Database session.

    Returns:
        Status dictionary with service and database status.
    """
    logger.debug("Health check requested")
    try:
        # Проверка доступности БД
        db.execute(text("SELECT 1"))
        logger.debug("Health check: database connected")
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        logger.error(
            "Health check failed: database disconnected",
            extra={"error": str(e)},
            exc_info=True,
        )
        return {"status": "error", "database": "disconnected"}
