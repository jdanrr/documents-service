"""Mappers de autorizaciones: schema <-> dominio <-> evento.

El payload del evento NO depende de las entidades internas.
"""

from app.domain import domain_events as events
from app.domain.entities import Authorization


def domain_to_response(entity: Authorization) -> dict:
    """Convierte entidad a dict de respuesta (el router lo pasa al schema)."""
    # TODO: mapear auth_id -> authId, issued_at -> issuedAt, status.value.
    raise NotImplementedError


def domain_to_domain_event(entity: Authorization, correlation_id: str) -> events.AuthorizationIssued:
    """Convierte entidad a evento de dominio para publicar."""
    # TODO: construir AuthorizationIssued con los campos del evento.
    raise NotImplementedError
