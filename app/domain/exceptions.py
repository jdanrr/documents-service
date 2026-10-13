"""Excepciones de dominio (sin dependencias de framework)."""


class DomainError(Exception):
    """Error base del dominio."""


class DocumentNotFoundError(DomainError):
    """El documento solicitado no existe."""

    # TODO: incluir document_id / document_type como atributos.


class InvalidDocumentOperationError(DomainError):
    """Operación no permitida sobre el documento (p. ej. UPDATE sin cambios)."""


class DocumentPublishError(DomainError):
    """Falló la publicación del evento de dominio (la lanza la aplicación)."""
