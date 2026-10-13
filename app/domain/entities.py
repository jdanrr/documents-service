"""Entidades del dominio (dataclasses puras, solo librería estándar).

Toda validación vive aquí y lanza excepciones de dominio específicas.
"""

from dataclasses import dataclass
from datetime import datetime

from app.domain.enums import DocumentStatus
from app.domain.exceptions import (
    InvalidDateOrderError,
    InvalidFieldError,
    InvalidStatusTransitionError,
)


def _require_text(value: str, field_name: str) -> str:
    """Valida texto obligatorio (no vacío ni solo espacios)."""
    if not isinstance(value, str) or not value.strip():
        raise InvalidFieldError(field_name, "es obligatorio y no puede estar vacío")
    return value


def _require_user_id(user_id: str) -> str:
    """Valida la referencia al usuario (obligatoria, vive en Profile)."""
    if not isinstance(user_id, str) or not user_id.strip():
        raise InvalidFieldError("user_id", "es obligatorio")
    return user_id


def _require_utc(moment: datetime, field_name: str) -> datetime:
    """Valida que el instante tenga zona horaria y sea UTC."""
    if not isinstance(moment, datetime) or moment.tzinfo is None:
        raise InvalidFieldError(field_name, "debe tener zona horaria")
    if moment.utcoffset() is None or moment.utcoffset().total_seconds() != 0:  # type: ignore[union-attr]
        raise InvalidFieldError(field_name, "debe estar en UTC")
    return moment


def _check_transition(current: DocumentStatus, attempted: DocumentStatus) -> DocumentStatus:
    """Valida ISSUED -> SENT | FAILED; SENT y FAILED son finales."""
    allowed = {
        DocumentStatus.ISSUED: (DocumentStatus.SENT, DocumentStatus.FAILED),
    }
    if attempted not in allowed.get(current, ()):
        raise InvalidStatusTransitionError(current.value, attempted.value)
    return attempted


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

    def __post_init__(self) -> None:
        _require_user_id(self.user_id)
        _require_text(self.procedure, "procedure")
        _require_text(self.doctor, "doctor")
        _require_text(self.location, "location")
        _require_utc(self.issued_at, "issued_at")

    def mark_sent(self) -> None:
        """Marca la autorización como enviada (ISSUED -> SENT)."""
        self.status = _check_transition(self.status, DocumentStatus.SENT)

    def mark_failed(self) -> None:
        """Marca fallido el envío (ISSUED -> FAILED)."""
        self.status = _check_transition(self.status, DocumentStatus.FAILED)


@dataclass
class AffiliationCertificate:
    """Certificado de afiliación de un usuario."""

    cert_id: str
    user_id: str
    issued_at: datetime
    status: DocumentStatus = DocumentStatus.ISSUED

    def __post_init__(self) -> None:
        _require_user_id(self.user_id)
        _require_utc(self.issued_at, "issued_at")

    def mark_sent(self) -> None:
        """Marca el certificado como enviado (ISSUED -> SENT)."""
        self.status = _check_transition(self.status, DocumentStatus.SENT)

    def mark_failed(self) -> None:
        """Marca fallido el envío (ISSUED -> FAILED)."""
        self.status = _check_transition(self.status, DocumentStatus.FAILED)


@dataclass
class MedicalHistoryRecord:
    """Registro individual del historial médico."""

    record_id: str
    user_id: str
    category: str
    description: str
    added_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        _require_user_id(self.user_id)
        _require_text(self.category, "category")
        _require_text(self.description, "description")
        _require_utc(self.added_at, "added_at")
        _require_utc(self.updated_at, "updated_at")
        if self.updated_at < self.added_at:
            raise InvalidDateOrderError()

    def update(self, category: str, description: str, now: datetime) -> None:
        """Actualiza el registro (el dueño se valida en el caso de uso)."""
        _require_text(category, "category")
        _require_text(description, "description")
        _require_utc(now, "updated_at")
        if now < self.added_at:
            raise InvalidDateOrderError()
        self.category = category
        self.description = description
        self.updated_at = now


@dataclass
class MedicalHistoryExport:
    """Exportación del historial a PDF (solo metadatos; el binario va al storage)."""

    pdf_id: str
    user_id: str
    record_count: int
    generated_at: datetime

    def __post_init__(self) -> None:
        _require_user_id(self.user_id)
        if not isinstance(self.record_count, int) or self.record_count < 0:
            raise InvalidFieldError("record_count", "debe ser un entero mayor o igual a cero")
        _require_utc(self.generated_at, "generated_at")
