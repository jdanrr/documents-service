"""Mappers de certificados: dominio -> schema."""

from app.domain.entities import AffiliationCertificate
from app.infrastructure.api.schemas.certificates import CertificateResponse


def domain_to_response(entity: AffiliationCertificate) -> CertificateResponse:
    """Convierte la entidad a respuesta 201."""
    return CertificateResponse(
        certificate_id=entity.cert_id,
        issued_at=entity.issued_at,
        affiliation_start_date=entity.affiliation_start_date,
    )
