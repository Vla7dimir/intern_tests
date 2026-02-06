"""Device models for AB testing."""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from app.db.connection import Base


def _utc_now() -> datetime:
    """Get current UTC datetime.

    Returns:
        Current datetime with UTC timezone.
    """
    return datetime.now(timezone.utc)


class Device(Base):
    """Device model representing a device participating in experiments."""

    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    device_token = Column(String, unique=True, nullable=False, index=True)
    first_seen_at = Column(
        DateTime(timezone=True),
        default=_utc_now,
        nullable=False,
        index=True,
    )


class DeviceExperiment(Base):
    """Device experiment assignment model linking devices to experiment values."""

    __tablename__ = "device_experiments"

    id = Column(Integer, primary_key=True, index=True)  # noqa: A003
    device_token = Column(String, nullable=False, index=True)
    experiment_key = Column(String, nullable=False, index=True)
    experiment_value = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=_utc_now, index=True)

    __table_args__ = (
        {"sqlite_autoincrement": True},
    )
