"""Migration 3/4: create experiment_options table (1 entity = 1 migration)."""

from typing import Optional, Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "b2c3d4e5f6a7"
down_revision: Optional[str] = "a1b2c3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
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
    op.create_index(op.f("ix_experiment_options_id"), "experiment_options", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_experiment_options_id"), table_name="experiment_options")
    op.drop_index(
        op.f("ix_experiment_options_experiment_key"),
        table_name="experiment_options",
    )
    op.drop_table("experiment_options")
