"""Caso de uso: generar certificado de afiliación."""

from app.application.ports.input.use_cases import GenerateAffiliationCertificateUseCase
from app.application.ports.output.event_publisher_port import EventPublisherPort
from app.application.ports.output.repository_ports import CertificateRepository
from app.domain.entities import AffiliationCertificate


class GenerateAffiliationCertificateUseCaseImpl(GenerateAffiliationCertificateUseCase):
    """Orquesta dominio + puertos para generar el certificado."""

    def __init__(
        self,
        repository: CertificateRepository,
        publisher: EventPublisherPort,
    ) -> None:
        self._repository = repository
        self._publisher = publisher

    async def execute(self, user_id: str, correlation_id: str) -> AffiliationCertificate:
        # TODO: 1) crear entidad AffiliationCertificate (uuid + now UTC + ISSUED).
        # TODO: 2) guardar con repository.save().
        # TODO: 3) mapear a evento CertificateGenerated.
        # TODO: 4) publicar con publisher.publish_certificate_generated().
        # TODO: 5) publicar DocumentsUpdated (CREATE) para auditoría.
        raise NotImplementedError
