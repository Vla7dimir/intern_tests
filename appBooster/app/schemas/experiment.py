"""API response schemas for experiments."""

from typing import Dict, Optional

from pydantic import BaseModel, Field


class ExperimentResponse(BaseModel):
    """Response with assigned experiment values (keys = experiment_key)."""

    button_color: Optional[str] = Field(None, description="Assigned button color value")
    price: Optional[str] = Field(None, description="Assigned price value")


class DistributionItem(BaseModel):
    """One option in experiment statistics: count, weight, percentage."""

    count: int = Field(..., description="Number of devices with this option")
    weight: int = Field(..., description="Weight of this option")
    percentage: float = Field(..., description="Percentage of devices with this option")


class StatisticsResponse(BaseModel):
    """Statistics for one experiment: key, total devices, distribution by options."""

    experiment_key: str = Field(..., description="Experiment key identifier")
    total_devices: int = Field(..., description="Total number of devices in experiment")
    distribution: Dict[str, DistributionItem] = Field(
        ...,
        description="Distribution of devices across experiment options",
    )
