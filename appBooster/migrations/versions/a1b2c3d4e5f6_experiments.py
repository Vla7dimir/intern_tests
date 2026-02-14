"""Migration 2/4: create experiments table (1 entity = 1 migration)."""

from typing import Optional, Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "a1b2c3d4e5f6"
down_revision: Optional[str] = "d8f3299607ba"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "experiments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("key", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_experiments_id"), "experiments", ["id"], unique=False)
    op.create_index(op.f("ix_experiments_key"), "experiments", ["key"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_experiments_key"), table_name="experiments")
    op.drop_index(op.f("ix_experiments_id"), table_name="experiments")
    op.drop_table("experiments")
