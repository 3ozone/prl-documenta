"""add_worker_fields_to_documents

Revision ID: 3f5c2d9a1e8b
Revises: 2e3a1b8c4d7f
Create Date: 2026-05-28 03:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3f5c2d9a1e8b"
down_revision: Union[str, Sequence[str], None] = "2e3a1b8c4d7f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add worker-specific columns to documents table."""
    op.add_column("documents", sa.Column("nombre_trabajador", sa.String(length=255), nullable=True))
    op.add_column("documents", sa.Column("dni", sa.String(length=20), nullable=True))
    op.add_column("documents", sa.Column("puesto", sa.String(length=255), nullable=True))
    op.add_column("documents", sa.Column("tipo_documento", sa.String(length=50), nullable=True))


def downgrade() -> None:
    """Remove worker-specific columns from documents table."""
    op.drop_column("documents", "nombre_trabajador")
    op.drop_column("documents", "dni")
    op.drop_column("documents", "puesto")
    op.drop_column("documents", "tipo_documento")
