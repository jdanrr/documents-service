"""Entidades internas del dominio (dataclasses estándar)."""

from dataclasses import dataclass
from datetime import datetime

from app.domain.enums import DocumentStatus


@dataclass
class Authorization:
    """Autorización médica asociada manualmente a un perfil."""

    auth_id: str
    user_id: str  # Referencia opaca; NO se consulta a Profile en tiempo real.
    procedure: str  # Dato ficticio.
    doctor: str  # Dato ficticio.
    location: str  # Dato ficticio.
    issued_at: datetime
    status: DocumentStatus = DocumentStatus.ISSUED
    # TODO: métodos de dominio si se necesitan (p. ej. mark_sent / mark_failed).


@dataclass
class AffiliationCertificate:
    """Certificado de afiliación de un usuario."""

    cert_id: str
    user_id: str
    issued_at: datetime
    status: DocumentStatus = DocumentStatus.ISSUED
    # TODO: métodos de dominio si se necesitan.


@dataclass
class MedicalHistoryRecord:
    """Registro individual del historial médico."""

    record_id: str
    user_id: str
    category: str
    description: str
    added_at: datetime
    updated_at: datetime
    # TODO: método update(category, description, now) si se quiere lógica en dominio.


@dataclass
class MedicalHistoryExport:
    """Exportación del historial a PDF (solo metadatos; el binario va al storage)."""

    pdf_id: str
    user_id: str
    record_count: int
    generated_at: datetime
    # TODO: validación de dominio (record_count >= 0) si se requiere.
