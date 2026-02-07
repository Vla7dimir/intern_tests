"""FastAPI entry point: Hacker News proxy app and router."""

from contextlib import asynccontextmanager
from typing import Union
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse, PlainTextResponse
from starlette.responses import Response

from app.logger import get_logger, setup_logging
from app.proxy.processor import process_html
from config.settings import settings

setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Shared HTTP client for upstream (connection pooling), closed on shutdown."""
    async with httpx.AsyncClient(
        follow_redirects=True,
        timeout=settings.request_timeout,
    ) as client:
        app.state.httpx_client = client
        yield
    app.state.httpx_client = None  # type: ignore[assignment]


app = FastAPI(title="Hacker News Proxy", lifespan=lifespan)
router = APIRouter()


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


def _build_target_url(path: str, query_params: dict) -> str:
    """Build upstream URL with correctly encoded query parameters.

    Args:
        path: Request path.
        query_params: Query parameters dictionary.

    Returns:
        Complete upstream URL.

    Raises:
        ValueError: If path contains invalid characters or is too long.
    """
    if len(path) > 2048:
        raise ValueError("Path too long")
    if ".." in path or path.startswith("//"):
        raise ValueError("Invalid path")
    base_url = settings.hn_base_url.rstrip("/")
    base = f"{base_url}/{path.lstrip('/')}" if path else base_url
    if query_params:
        return f"{base}?{urlencode(query_params, doseq=True)}"
    return base


def _build_response(
    response: httpx.Response,
    proxy_url: str,
) -> Union[HTMLResponse, Response]:
    """Build response for client: HTML via process_html, rest as-is.

    Args:
        response: httpx response from upstream.
        proxy_url: Proxy base URL for rewriting links.

    Returns:
        HTMLResponse for HTML content, Response for other content types.

    Raises:
        ValueError: If response is too large or processing fails.
    """
    content_type = response.headers.get("content-type", "").lower()
    content_length = len(response.content)
    max_size = settings.max_response_size
    if content_length > max_size:
        logger.warning(
            "Response too large",
            extra={"size": content_length, "max_size": max_size},
        )
        raise ValueError("Response too large")
    if "text/html" in content_type:
        try:
            processed_html = process_html(response.text, proxy_url)
            return HTMLResponse(
                content=processed_html, status_code=response.status_code
            )
        except Exception as e:
            logger.error(
                "Failed to process HTML",
                extra={"error": str(e)},
                exc_info=True,
            )
            # Return original HTML on processing error
            return HTMLResponse(
                content=response.text, status_code=response.status_code
            )
    return Response(
        content=response.content,
        status_code=response.status_code,
        media_type=content_type,
    )


@router.api_route(
    "/{path:path}",
    methods=["GET", "POST"],
    response_model=None,
    responses={
        200: {"description": "Success (HTML or content from HN)"},
        400: {"description": "Bad Request (invalid path)"},
        405: {"description": "Method Not Allowed (only GET/POST)"},
        413: {"description": "Request Entity Too Large"},
        502: {"description": "Bad Gateway — upstream (HN) error"},
        503: {"description": "Service Unavailable (client not initialized)"},
        504: {"description": "Gateway Timeout"},
    },
)
async def proxy(
    request: Request, path: str
) -> Union[HTMLResponse, Response, PlainTextResponse]:
    """Proxy request to Hacker News; return modified HTML or content.

    Args:
        request: FastAPI request object.
        path: Request path to proxy.

    Returns:
        HTMLResponse for HTML content, Response for other types,
        PlainTextResponse for errors.

    Raises:
        HTTPException: For validation errors (400, 405, 503).
    """
    http_client = getattr(request.app.state, "httpx_client", None)
    if http_client is None:
        logger.error("httpx_client not initialized")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service Unavailable",
        )

    proxy_url = str(request.base_url).rstrip("/")
    query_params = dict(request.query_params)

    try:
        target_url = _build_target_url(path, query_params)
    except ValueError as e:
        logger.warning("Invalid path", extra={"path": path, "error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid path",
        ) from e

    logger.debug(
        "Proxying request",
        extra={
            "method": request.method,
            "path": path,
            "target_url": target_url,
        },
    )

    try:
        if request.method == "GET":
            response = await http_client.get(target_url)
        elif request.method == "POST":
            body = await request.body()
            if len(body) > settings.max_response_size:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail="Request body too large",
                )
            response = await http_client.post(target_url, content=body)
        else:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail="Method Not Allowed",
            )

        response.raise_for_status()
        return _build_response(response, proxy_url)

    except httpx.TimeoutException as e:
        logger.warning(
            "Upstream timeout",
            extra={"target_url": target_url, "error": str(e)},
        )
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Upstream timeout",
        ) from e
    except httpx.HTTPStatusError as e:
        logger.warning(
            "Upstream HTTP error",
            extra={
                "target_url": target_url,
                "status_code": e.response.status_code,
            },
        )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Upstream error",
        ) from e
    except httpx.HTTPError as e:
        logger.warning(
            "Upstream error",
            extra={"target_url": target_url, "error": str(e)},
        )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Error fetching page from upstream",
        ) from e
    except ValueError as e:
        logger.error(
            "Response processing error",
            extra={"target_url": target_url, "error": str(e)},
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Error processing response",
        ) from e


app.include_router(router)
