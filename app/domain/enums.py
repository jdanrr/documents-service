"""Enums del dominio (librería estándar, sin dependencias externas)."""

from enum import Enum


class DocumentStatus(str, Enum):
    """Estado de una autorización o certificado."""

    ISSUED = "ISSUED"
    SENT = "SENT"
    FAILED = "FAILED"


class DocumentType(str, Enum):
    """Tipo de documento para el evento de auditoría DocumentsUpdated."""

    AUTHORIZATION = "AUTHORIZATION"
    AFFILIATION_CERTIFICATE = "AFFILIATION_CERTIFICATE"
    MEDICAL_HISTORY_PDF = "MEDICAL_HISTORY_PDF"


class DocumentOperation(str, Enum):
    """Operación realizada sobre un documento."""

    CREATE = "CREATE"
    UPDATE = "UPDATE"
