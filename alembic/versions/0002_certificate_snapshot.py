"""Migración 0002: profile_snapshots y columnas nuevas del certificado.

Supuesto: affiliation_certificates está vacía en todos los entornos
(cada cambio de estado emite un certificado nuevo, no hay backfill).

Revision ID: 0002_certificate_snapshot
"""

import sqlalchemy as sa
from alembic import op

revision = "0002_certificate_snapshot"
down_revision = "0001_initial_tables"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "profile_snapshots",
        sa.Column("user_id", sa.String(64), primary_key=True),
        sa.Column("document_type", sa.String(10), nullable=False),
        sa.Column("document_number", sa.String(30), nullable=False),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=False),
        sa.Column("affiliation_start_date", sa.DateTime(timezone=True), nullable=False),
    )
    op.add_column(
        "affiliation_certificates",
        sa.Column("affiliation_start_date", sa.DateTime(timezone=True), nullable=False),
    )
    op.add_column(
        "affiliation_certificates",
        sa.Column("file_key", sa.Text(), nullable=False),
    )


def downgrade() -> None:
    op.drop_column("affiliation_certificates", "file_key")
    op.drop_column("affiliation_certificates", "affiliation_start_date")
    op.drop_table("profile_snapshots")
