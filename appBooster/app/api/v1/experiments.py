"""Experiments API endpoints."""

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.experiments.manager import ExperimentManager
from app.logger import get_logger
from app.schemas.experiment import ExperimentResponse

logger = get_logger(__name__)

router = APIRouter(tags=["Experiments"])


@router.get(
    "/experiments",
    response_model=ExperimentResponse,
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
        experiment_values = manager.get_experiments_for_device(device_token)
        logger.info(
            "Experiments retrieved",
            extra={
                "device_token": device_token,
                "experiments": list(experiment_values.keys()),
            },
        )
        return ExperimentResponse(**experiment_values)
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
