"""Eventos de dominio (hechos internos, sin sobre EventBridge).

El sobre estándar (source/detail-type/metadata/data) se arma en
la capa de infraestructura (messaging/contracts), no aquí.
"""

from dataclasses import dataclass
from datetime import datetime

from app.domain.enums import DocumentOperation, DocumentType


@dataclass(frozen=True)
class AuthorizationIssued:
    """Se emitió una autorización médica."""

    auth_id: str
    user_id: str
    procedure: str
    doctor: str
    location: str
    issued_at: datetime
    correlation_id: str


@dataclass(frozen=True)
class CertificateGenerated:
    """Se generó un certificado de afiliación."""

    cert_id: str
    user_id: str
    issued_at: datetime
    correlation_id: str


@dataclass(frozen=True)
class MedicalHistoryPdfGenerated:
    """Se generó el PDF del historial médico."""

    pdf_id: str
    user_id: str
    record_count: int
    generated_at: datetime
    correlation_id: str


@dataclass(frozen=True)
class DocumentsUpdated:
    """Evento de auditoría genérico (sin consumidor por ahora)."""

    document_id: str
    document_type: DocumentType
    user_id: str
    operation: DocumentOperation
    updated_at: datetime
    correlation_id: str
