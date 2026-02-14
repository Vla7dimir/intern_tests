"""Migration 1/4: create devices table (1 entity = 1 migration)."""

from typing import Optional, Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "d8f3299607ba"
down_revision: Optional[str] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "devices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("device_token", sa.String(), nullable=False),
        sa.Column("first_seen_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_devices_device_token"), "devices", ["device_token"], unique=True)
    op.create_index(op.f("ix_devices_id"), "devices", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_devices_id"), table_name="devices")
    op.drop_index(op.f("ix_devices_device_token"), table_name="devices")
    op.drop_table("devices")
