"""Seed initial experiments (button_color, price) from env.

Options format: value1:weight1,value2:weight2,...
Env: BUTTON_COLOR_OPTIONS, PRICE_OPTIONS (optional).
"""

import os
from datetime import datetime, timezone
from typing import List, Optional, Sequence, Tuple, Union

import alembic.op as op
import sqlalchemy as sa


revision: str = "b1c2d3e4f5a6"
down_revision: Optional[str] = "d8f3299607ba"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _parse_options(s: str) -> List[Tuple[str, int]]:
    """Parse 'value1:weight1,value2:weight2' into [(value, weight), ...]."""
    result = []
    for part in s.strip().split(','):
        part = part.strip()
        if ':' in part:
            val, w = part.rsplit(':', 1)
            try:
                result.append((val.strip(), int(w.strip())))
            except ValueError:
                continue
    return result


def _seed_experiment(conn, key: str, options_str: str) -> None:
    """Seed experiment with options.

    Args:
        conn: Database connection.
        key: Experiment key.
        options_str: Options string in format 'value1:weight1,value2:weight2'.
    """
    r = conn.execute(
        sa.text("SELECT id FROM experiments WHERE key = :key"),
        {"key": key},
    )
    if r.fetchone() is not None:
        return
    now = datetime.now(timezone.utc)
    conn.execute(
        sa.text(
            "INSERT INTO experiments (key, created_at) VALUES (:key, :created_at)"
        ),
        {"key": key, "created_at": now},
    )
    r = conn.execute(
        sa.text("SELECT id FROM experiments WHERE key = :key"),
        {"key": key},
    )
    row = r.fetchone()
    if not row:
        return
    for value, weight in _parse_options(options_str):
        conn.execute(
            sa.text(
                "INSERT INTO experiment_options (experiment_key, value, weight) "
                "VALUES (:experiment_key, :value, :weight)"
            ),
            {"experiment_key": key, "value": value, "weight": weight},
        )


def upgrade() -> None:
    """Upgrade database: seed initial experiments."""
    conn = op.get_bind()
    button_opts = os.getenv(
        "BUTTON_COLOR_OPTIONS",
        "#FF0000:33,#00FF00:33,#0000FF:34",
    )
    price_opts = os.getenv("PRICE_OPTIONS", "10:75,20:10,50:5,5:10")
    _seed_experiment(conn, "button_color", button_opts)
    _seed_experiment(conn, "price", price_opts)


def downgrade() -> None:
    """Downgrade database: remove initial experiments."""
    op.execute(
        sa.text(
            "DELETE FROM experiment_options "
            "WHERE experiment_key IN ('button_color', 'price')"
        )
    )
    op.execute(
        sa.text(
            "DELETE FROM experiments WHERE key IN ('button_color', 'price')"
        )
    )
