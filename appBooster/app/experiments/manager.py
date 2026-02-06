"""Experiment manager: device assignment and statistics."""

import random
from typing import Any, Dict, List, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.logger import get_logger
from app.models.device import Device, DeviceExperiment
from app.models.experiment import Experiment, ExperimentOption

logger = get_logger(__name__)


def get_experiments(db: Session) -> List[Experiment]:
    """Return all experiments from the database.

    Args:
        db: Database session.

    Returns:
        List of all experiments.
    """
    return db.query(Experiment).all()


def get_options_for_experiment(
    db: Session,
    experiment_key: str,
) -> List[ExperimentOption]:
    """Return all options for a given experiment key.

    Args:
        db: Database session.
        experiment_key: Key of the experiment.

    Returns:
        List of experiment options ordered by ID.
    """
    return (
        db.query(ExperimentOption)
        .filter(ExperimentOption.experiment_key == experiment_key)
        .order_by(ExperimentOption.id)
        .all()
    )


class ExperimentManager:
    """Experiment manager for device assignment and statistics collection."""

    def __init__(self, db: Session) -> None:
        """Initialize experiment manager.

        Args:
            db: Database session.
        """
        self.db = db

    def get_or_create_device(self, device_token: str) -> Device:
        """Get device by token or create new one.

        Args:
            device_token: Unique device token identifier.

        Returns:
            Device instance.

        Raises:
            IntegrityError: If device creation fails due to constraint violation.
        """
        logger.debug("Getting or creating device", extra={"device_token": device_token})
        device = self.db.query(Device).filter(Device.device_token == device_token).first()
        if not device:
            device = Device(device_token=device_token)
            try:
                self.db.add(device)
                self.db.commit()
                self.db.refresh(device)
                logger.info("Device created", extra={"device_token": device_token})
            except IntegrityError as e:
                self.db.rollback()
                logger.error(
                    "Failed to create device",
                    extra={"device_token": device_token, "error": str(e)},
                    exc_info=True,
                )
                raise
            except Exception as e:
                self.db.rollback()
                logger.error(
                    "Unexpected error creating device",
                    extra={"device_token": device_token, "error": str(e)},
                    exc_info=True,
                )
                raise
        else:
            logger.debug("Device found", extra={"device_token": device_token})
        return device

    def get_experiments_for_device(self, device_token: str) -> Dict[str, str]:
        """Get experiment assignments for device.

        Args:
            device_token: Device token identifier.

        Returns:
            Dictionary mapping experiment_key to assigned value.

        Raises:
            Exception: If database operation fails.
        """
        logger.debug("Getting experiments for device", extra={"device_token": device_token})
        try:
            device = self.get_or_create_device(device_token)
            device_first_seen = device.first_seen_at

            experiments = {}
            existing_assignments = (
                self.db.query(DeviceExperiment)
                .filter(DeviceExperiment.device_token == device_token)
                .all()
            )
            existing_dict = {
                e.experiment_key: e.experiment_value for e in existing_assignments
            }

            all_experiments = get_experiments(self.db)
            for exp in all_experiments:
                if exp.key in existing_dict:
                    experiments[exp.key] = existing_dict[exp.key]
                elif exp.created_at <= device_first_seen:
                    value = self._assign_experiment(device_token, exp.key)
                    if value:
                        experiments[exp.key] = value

            logger.info(
                "Experiments retrieved for device",
                extra={
                    "device_token": device_token,
                    "experiments_count": len(experiments),
                },
            )
            return experiments
        except Exception as e:
            logger.error(
                "Failed to get experiments for device",
                extra={"device_token": device_token, "error": str(e)},
                exc_info=True,
            )
            raise

    def _assign_experiment(self, device_token: str, experiment_key: str) -> Optional[str]:
        """Assign experiment option by weights and save to device_experiments.

        Args:
            device_token: Device token identifier.
            experiment_key: Experiment key identifier.

        Returns:
            Assigned experiment value or None if assignment fails.

        Raises:
            IntegrityError: If assignment creation fails due to constraint violation.
        """
        logger.debug(
            "Assigning experiment",
            extra={"device_token": device_token, "experiment_key": experiment_key},
        )
        options = get_options_for_experiment(self.db, experiment_key)

        if not options:
            logger.warning(
                "No options found for experiment",
                extra={"experiment_key": experiment_key},
            )
            return None

        total_weight = sum(opt.weight for opt in options)
        if total_weight == 0:
            logger.warning(
                "Total weight is zero for experiment",
                extra={"experiment_key": experiment_key},
            )
            return None

        random_value = random.randint(1, total_weight)
        cumulative = 0

        for option in options:
            cumulative += option.weight
            if random_value <= cumulative:
                assignment = DeviceExperiment(
                    device_token=device_token,
                    experiment_key=experiment_key,
                    experiment_value=option.value,
                )
                try:
                    self.db.add(assignment)
                    self.db.commit()
                    logger.info(
                        "Experiment assigned",
                        extra={
                            "device_token": device_token,
                            "experiment_key": experiment_key,
                            "value": option.value,
                        },
                    )
                    return option.value
                except IntegrityError as e:
                    self.db.rollback()
                    logger.warning(
                        "Assignment already exists or constraint violation",
                        extra={
                            "device_token": device_token,
                            "experiment_key": experiment_key,
                            "error": str(e),
                        },
                    )
                    # Возвращаем существующее значение или None
                    existing = (
                        self.db.query(DeviceExperiment)
                        .filter(
                            DeviceExperiment.device_token == device_token,
                            DeviceExperiment.experiment_key == experiment_key,
                        )
                        .first()
                    )
                    return existing.experiment_value if existing else None
                except Exception as e:
                    self.db.rollback()
                    logger.error(
                        "Failed to assign experiment",
                        extra={
                            "device_token": device_token,
                            "experiment_key": experiment_key,
                            "error": str(e),
                        },
                        exc_info=True,
                    )
                    raise

        # Fallback при некорректных весах
        logger.warning(
            "Using fallback option",
            extra={"experiment_key": experiment_key},
        )
        return options[-1].value

    def get_statistics(self) -> List[Dict[str, Any]]:
        """Get statistics for all experiments: distribution by options (count, weight, %).

        Returns:
            List of dictionaries with experiment statistics.

        Raises:
            Exception: If database operation fails.
        """
        logger.debug("Getting statistics")
        try:
            experiments = get_experiments(self.db)
            stats = []

            for exp in experiments:
                options = get_options_for_experiment(self.db, exp.key)

                total_devices = (
                    self.db.query(DeviceExperiment)
                    .filter(DeviceExperiment.experiment_key == exp.key)
                    .count()
                )

                distribution = {}
                for option in options:
                    count = (
                        self.db.query(DeviceExperiment)
                        .filter(
                            DeviceExperiment.experiment_key == exp.key,
                            DeviceExperiment.experiment_value == option.value,
                        )
                        .count()
                    )
                    percentage = round(
                        (count / total_devices * 100) if total_devices > 0 else 0,
                        2,
                    )
                    distribution[option.value] = {
                        "count": count,
                        "weight": option.weight,
                        "percentage": percentage,
                    }

                stats.append(
                    {
                        "experiment_key": exp.key,
                        "total_devices": total_devices,
                        "distribution": distribution,
                    }
                )

            logger.info("Statistics retrieved", extra={"experiments_count": len(stats)})
            return stats
        except Exception as e:
            logger.error("Failed to get statistics", extra={"error": str(e)}, exc_info=True)
            raise
