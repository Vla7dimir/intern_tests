"""Migration 4/4: create device_experiments table (1 entity = 1 migration)."""

from typing import Optional, Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "c3d4e5f6a7b8"
down_revision: Optional[str] = "b2c3d4e5f6a7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
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


def downgrade() -> None:
    op.drop_index(op.f("ix_device_experiments_id"), table_name="device_experiments")
    op.drop_index(
        op.f("ix_device_experiments_experiment_key"),
        table_name="device_experiments",
    )
    op.drop_index(
        op.f("ix_device_experiments_device_token"),
        table_name="device_experiments",
    )
    op.drop_table("device_experiments")
