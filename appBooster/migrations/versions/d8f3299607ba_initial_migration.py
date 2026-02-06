from typing import Optional, Sequence, Union

import sqlalchemy as sa
from alembic import op



revision: str = "d8f3299607ba"
down_revision: Optional[str] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade database: create initial tables."""
    op.create_table(
        "device_experiments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("device_token", sa.String(), nullable=False),
        sa.Column("experiment_key", sa.String(), nullable=False),
        sa.Column("experiment_value", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sqlite_autoincrement=True,
    )
    op.create_index(
        op.f("ix_device_experiments_device_token"),
        "device_experiments",
        ["device_token"],
        unique=False,
    )
    op.create_index(
        op.f("ix_device_experiments_experiment_key"),
        "device_experiments",
        ["experiment_key"],
        unique=False,
    )
    op.create_index(
        op.f("ix_device_experiments_id"),
        "device_experiments",
        ["id"],
        unique=False,
    )
    op.create_table(
        "devices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("device_token", sa.String(), nullable=False),
        sa.Column("first_seen_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_devices_device_token"),
        "devices",
        ["device_token"],
        unique=True,
    )
    op.create_index(
        op.f("ix_devices_id"),
        "devices",
        ["id"],
        unique=False,
    )
    op.create_table(
        "experiment_options",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("experiment_key", sa.String(), nullable=False),
        sa.Column("value", sa.String(), nullable=False),
        sa.Column("weight", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_experiment_options_experiment_key"),
        "experiment_options",
        ["experiment_key"],
        unique=False,
    )
    op.create_index(
        op.f("ix_experiment_options_id"),
        "experiment_options",
        ["id"],
        unique=False,
    )
    op.create_table(
        "experiments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("key", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_experiments_id"),
        "experiments",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_experiments_key"),
        "experiments",
        ["key"],
        unique=True,
    )


def downgrade() -> None:
    """Downgrade database: drop all tables."""
    op.drop_index(op.f("ix_experiments_key"), table_name="experiments")
    op.drop_index(op.f("ix_experiments_id"), table_name="experiments")
    op.drop_table("experiments")
    op.drop_index(
        op.f("ix_experiment_options_id"),
        table_name="experiment_options",
    )
    op.drop_index(
        op.f("ix_experiment_options_experiment_key"),
        table_name="experiment_options",
    )
    op.drop_table("experiment_options")
    op.drop_index(op.f("ix_devices_id"), table_name="devices")
    op.drop_index(op.f("ix_devices_device_token"), table_name="devices")
    op.drop_table("devices")
    op.drop_index(
        op.f("ix_device_experiments_id"),
        table_name="device_experiments",
    )
    op.drop_index(
        op.f("ix_device_experiments_experiment_key"),
        table_name="device_experiments",
    )
    op.drop_index(
        op.f("ix_device_experiments_device_token"),
        table_name="device_experiments",
    )
    op.drop_table("device_experiments")
