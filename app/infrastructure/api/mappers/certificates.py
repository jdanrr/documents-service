"""Mappers de certificados: schema <-> dominio <-> evento."""

from app.domain import domain_events as events
from app.domain.entities import AffiliationCertificate


def domain_to_response(entity: AffiliationCertificate) -> dict:
    """Convierte entidad a dict de respuesta."""
    # TODO: mapear cert_id -> certId, issued_at -> issuedAt, status.value.
    raise NotImplementedError


def domain_to_domain_event(
    entity: AffiliationCertificate, correlation_id: str
) -> events.CertificateGenerated:
    """Convierte entidad a evento de dominio."""
    # TODO: construir CertificateGenerated.
    raise NotImplementedError
