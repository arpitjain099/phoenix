"""Create Platform Schema.

Revision ID: fc14296708b6
Revises:
Create Date: 2024-03-20 16:02:19.347915

"""
from typing import Sequence, Union

from alembic import op

revision: str = "fc14296708b6"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SCHEMA = "platform"


def upgrade() -> None:
    """Upgrade for fc14296708b6."""
    op.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}")


def downgrade() -> None:
    """Downgrade for fc14296708b6."""
    op.execute(f"DROP SCHEMA IF EXISTS {SCHEMA} CASCADE")
