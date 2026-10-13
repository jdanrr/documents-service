"""Modelos ORM (solo infraestructura; el dominio sigue con dataclasses puras).

Reglas: user_id es referencia opaca (índice, SIN FK a Profile), status con
CHECK (sin catálogos), PK UUID como texto, timestamps con zona horaria UTC.
"""

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.persistence.database import Base


def _uuid() -> str:
    """Genera un UUID v4 como texto (PK por defecto)."""
    return str(uuid.uuid4())


class AuthorizationModel(Base):
    """Tabla authorizations (autorizaciones médicas)."""

    __tablename__ = "authorizations"
    __table_args__ = (
        CheckConstraint("status IN ('ISSUED','SENT','FAILED')", name="ck_authorizations_status"),
        Index("ix_authorizations_user_id", "user_id"),
    )

    auth_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    user_id: Mapped[str] = mapped_column(String(64), nullable=False)  # Referencia, NO FK.
    procedure: Mapped[str] = mapped_column(String(255), nullable=False)
    doctor: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="ISSUED")


class AffiliationCertificateModel(Base):
    """Tabla affiliation_certificates (certificados de afiliación)."""

    __tablename__ = "affiliation_certificates"
    __table_args__ = (
        CheckConstraint("status IN ('ISSUED','SENT','FAILED')", name="ck_certificates_status"),
        Index("ix_affiliation_certificates_user_id", "user_id"),
    )

    cert_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    user_id: Mapped[str] = mapped_column(String(64), nullable=False)  # Referencia, NO FK.
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="ISSUED")


class MedicalHistoryRecordModel(Base):
    """Tabla medical_history_records (registros del historial)."""

    __tablename__ = "medical_history_records"
    __table_args__ = (Index("ix_medical_history_records_user_id", "user_id"),)

    record_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    user_id: Mapped[str] = mapped_column(String(64), nullable=False)  # Referencia, NO FK.
    category: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    added_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class MedicalHistoryExportModel(Base):
    """Tabla medical_history_exports (metadatos de PDFs generados)."""

    __tablename__ = "medical_history_exports"
    __table_args__ = (Index("ix_medical_history_exports_user_id", "user_id"),)

    pdf_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    user_id: Mapped[str] = mapped_column(String(64), nullable=False)  # Referencia, NO FK.
    record_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
