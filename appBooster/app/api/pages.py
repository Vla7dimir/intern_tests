"""HTML pages (non-API routes)."""

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.experiments.manager import ExperimentManager
from app.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(tags=["Pages"])

BASE_DIR = Path(__file__).resolve().parent.parent.parent
TEMPLATE_DIR = BASE_DIR / "templates"
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


@router.get(
    "/statistics",
    response_class=HTMLResponse,
    summary="Statistics HTML page",
    description="Get experiment statistics as HTML page",
    include_in_schema=False,
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
