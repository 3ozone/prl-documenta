"""add_equipment_fields_to_documents

Revision ID: 4a7b9c2d8e3f
Revises: 3f5c2d9a1e8b
Create Date: 2026-05-29 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4a7b9c2d8e3f"
down_revision: Union[str, Sequence[str], None] = "3f5c2d9a1e8b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add equipment-specific columns to documents table."""
    op.add_column("documents", sa.Column("id_equipo", sa.String(length=100), nullable=True))
    op.add_column("documents", sa.Column("nombre_equipo", sa.String(length=255), nullable=True))
    op.add_column("documents", sa.Column("numero_serie", sa.String(length=100), nullable=True))
    op.add_column("documents", sa.Column("ubicacion", sa.String(length=255), nullable=True))
    op.add_column("documents", sa.Column("subtipo", sa.String(length=50), nullable=True))
    op.add_column("documents", sa.Column("tipo_mantenimiento", sa.String(length=50), nullable=True))
    op.add_column("documents", sa.Column("empresa_mantenedora", sa.String(length=255), nullable=True))
    op.add_column("documents", sa.Column("fecha_proximo_mantenimiento", sa.Date(), nullable=True))
    op.add_column("documents", sa.Column("organismo_inspector", sa.String(length=255), nullable=True))
    op.add_column("documents", sa.Column("resultado_inspeccion", sa.String(length=50), nullable=True))
    op.add_column("documents", sa.Column("fecha_proxima_inspeccion", sa.Date(), nullable=True))


def downgrade() -> None:
    """Remove equipment-specific columns from documents table."""
    op.drop_column("documents", "id_equipo")
    op.drop_column("documents", "nombre_equipo")
    op.drop_column("documents", "numero_serie")
    op.drop_column("documents", "ubicacion")
    op.drop_column("documents", "subtipo")
    op.drop_column("documents", "tipo_mantenimiento")
    op.drop_column("documents", "empresa_mantenedora")
    op.drop_column("documents", "fecha_proximo_mantenimiento")
    op.drop_column("documents", "organismo_inspector")
    op.drop_column("documents", "resultado_inspeccion")
    op.drop_column("documents", "fecha_proxima_inspeccion")