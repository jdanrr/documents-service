"""Migración inicial: crea las 4 tablas de documents.

Revision ID: 0001_initial_tables
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial_tables"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "authorizations",
        sa.Column("auth_id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(64), nullable=False),
        sa.Column("procedure", sa.String(255), nullable=False),
        sa.Column("doctor", sa.String(255), nullable=False),
        sa.Column("location", sa.String(255), nullable=False),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(16), nullable=False, server_default="ISSUED"),
        sa.CheckConstraint("status IN ('ISSUED','SENT','FAILED')", name="ck_authorizations_status"),
    )
    op.create_index("ix_authorizations_user_id", "authorizations", ["user_id"])

    op.create_table(
        "affiliation_certificates",
        sa.Column("cert_id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(64), nullable=False),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(16), nullable=False, server_default="ISSUED"),
        sa.CheckConstraint("status IN ('ISSUED','SENT','FAILED')", name="ck_certificates_status"),
    )
    op.create_index("ix_affiliation_certificates_user_id", "affiliation_certificates", ["user_id"])

    op.create_table(
        "medical_history_records",
        sa.Column("record_id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(64), nullable=False),
        sa.Column("category", sa.String(128), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("added_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_medical_history_records_user_id", "medical_history_records", ["user_id"])

    op.create_table(
        "medical_history_exports",
        sa.Column("pdf_id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(64), nullable=False),
        sa.Column("record_count", sa.Integer, nullable=False, server_default="0"),
        sa.Column("generated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_medical_history_exports_user_id", "medical_history_exports", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_medical_history_exports_user_id", table_name="medical_history_exports")
    op.drop_table("medical_history_exports")
    op.drop_index("ix_medical_history_records_user_id", table_name="medical_history_records")
    op.drop_table("medical_history_records")
    op.drop_index("ix_affiliation_certificates_user_id", table_name="affiliation_certificates")
    op.drop_table("affiliation_certificates")
    op.drop_index("ix_authorizations_user_id", table_name="authorizations")
    op.drop_table("authorizations")
