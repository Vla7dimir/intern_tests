"""Statistics API endpoints."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.experiments.manager import ExperimentManager
from app.logger import get_logger
from app.schemas.experiment import StatisticsResponse

logger = get_logger(__name__)

router = APIRouter(tags=["Statistics"])


@router.get(
    "/statistics",
    response_model=List[StatisticsResponse],
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
