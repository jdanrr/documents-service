"""Excepciones de dominio (solo librería estándar, sin frameworks)."""


class DomainError(Exception):
    """Error base del dominio."""


class InvalidFieldError(DomainError):
    """Un campo tiene un valor inválido (vacío, ausente o mal formado)."""

    def __init__(self, field: str, reason: str) -> None:
        self.field = field
        self.reason = reason
        super().__init__(f"Campo inválido '{field}': {reason}.")


class InvalidDateOrderError(DomainError):
    """El orden cronológico de las fechas es inválido."""

    def __init__(self, message: str = "La fecha de actualización es anterior a la de creación.") -> None:
        super().__init__(message)


class InvalidStatusTransitionError(DomainError):
    """Transición de estado no permitida (SENT y FAILED son finales)."""

    def __init__(self, current: str, attempted: str) -> None:
        self.current = current
        self.attempted = attempted
        super().__init__(f"Transición inválida de '{current}' a '{attempted}'.")
