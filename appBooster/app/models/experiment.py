"""Experiment models for AB testing."""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from app.db.connection import Base


def _utc_now() -> datetime:
    """Get current UTC datetime.

    Returns:
        Current datetime with UTC timezone.
    """
    return datetime.now(timezone.utc)


class Experiment(Base):
    """Experiment model representing an AB test experiment."""

    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, index=True)  # noqa: A003
    key = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(
        DateTime(timezone=True),
        default=_utc_now,
        nullable=False,
        index=True,
    )


class ExperimentOption(Base):
    """Experiment option model representing a variant in an experiment."""

    __tablename__ = "experiment_options"

    id = Column(Integer, primary_key=True, index=True)  # noqa: A003
    experiment_key = Column(String, nullable=False, index=True)
    value = Column(String, nullable=False)
    weight = Column(Integer, nullable=False)
