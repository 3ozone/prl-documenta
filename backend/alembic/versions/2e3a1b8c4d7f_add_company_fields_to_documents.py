"""add_company_fields_to_documents

Revision ID: 2e3a1b8c4d7f
Revises: d81995aa6bdf
Create Date: 2026-05-28 02:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e3a1b8c4d7f'
down_revision: Union[str, Sequence[str], None] = 'd81995aa6bdf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add company-specific columns to documents table."""
    op.add_column('documents', sa.Column('razon_social', sa.String(length=255), nullable=True))
    op.add_column('documents', sa.Column('cif', sa.String(length=20), nullable=True))
    op.add_column('documents', sa.Column('actividad_economica', sa.String(length=255), nullable=True))
    op.add_column('documents', sa.Column('centro_trabajo', sa.String(length=255), nullable=True))


def downgrade() -> None:
    """Remove company-specific columns from documents table."""
    op.drop_column('documents', 'razon_social')
    op.drop_column('documents', 'cif')
    op.drop_column('documents', 'actividad_economica')
    op.drop_column('documents', 'centro_trabajo')