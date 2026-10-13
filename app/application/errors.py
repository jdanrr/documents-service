"""Errores de aplicación (sin lógica HTTP; los routers los mapean después)."""


class ApplicationError(Exception):
    """Error base de la capa de aplicación."""


class NotFound(ApplicationError):
    """El documento solicitado no existe."""

    def __init__(self, document_type: str, document_id: str) -> None:
        self.document_type = document_type
        self.document_id = document_id
        super().__init__(f"No existe {document_type} con id '{document_id}'.")


class Forbidden(ApplicationError):
    """El documento no pertenece al usuario que lo solicita."""

    def __init__(self, document_id: str) -> None:
        self.document_id = document_id
        super().__init__(f"El documento '{document_id}' pertenece a otro usuario.")


class EmptyMedicalHistory(ApplicationError):
    """El usuario no tiene registros para exportar."""

    def __init__(self, user_id: str) -> None:
        self.user_id = user_id
        super().__init__(f"El usuario '{user_id}' no tiene historial médico para exportar.")


class EventPublishError(ApplicationError):
    """Falló la publicación de eventos (lo guardado NO se revierte).

    TODO: el patrón Outbox resolvería esta ventana de inconsistencia; se omite
    TODO: a propósito por alcance académico (guardar primero, publicar después).
    """

    def __init__(self, message: str = "No se pudieron publicar los eventos.") -> None:
        super().__init__(message)
