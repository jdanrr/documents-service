"""Caso de uso: generar certificado de afiliación."""

from app.application.errors import EventPublishError
from app.application.ports.input.use_cases import (
    GenerateAffiliationCertificateCommand,
    GenerateAffiliationCertificateUseCase,
)
from app.application.ports.output.event_publisher_port import EventPublisherPort
from app.application.ports.output.repository_ports import CertificateRepository
from app.application.ports.output.system_ports import ClockPort, IdGeneratorPort
from app.domain import domain_events as events
from app.domain.entities import AffiliationCertificate
from app.domain.enums import DocumentOperation, DocumentType


class GenerateAffiliationCertificateUseCaseImpl(GenerateAffiliationCertificateUseCase):
    """Crea el certificado con ISSUED, lo guarda y publica sus eventos."""

    def __init__(
        self,
        repository: CertificateRepository,
        publisher: EventPublisherPort,
        clock: ClockPort,
        ids: IdGeneratorPort,
    ) -> None:
        self._repository = repository
        self._publisher = publisher
        self._clock = clock
        self._ids = ids

    async def execute(
        self, command: GenerateAffiliationCertificateCommand
    ) -> AffiliationCertificate:
        now = self._clock.now()
        certificate = AffiliationCertificate(
            cert_id=str(self._ids.new_id()),
            user_id=command.user_id,
            issued_at=now,
        )
        saved = await self._repository.save(certificate)
        outgoing = [
            events.CertificateGenerated(
                cert_id=saved.cert_id,
                user_id=saved.user_id,
                issued_at=saved.issued_at,
            ),
            events.DocumentsUpdated(
                document_id=saved.cert_id,
                document_type=DocumentType.AFFILIATION_CERTIFICATE,
                user_id=saved.user_id,
                operation=DocumentOperation.CREATE,
                updated_at=saved.issued_at,
            ),
        ]
        try:
            await self._publisher.publish(outgoing, command.correlation_id)
        except EventPublishError:
            raise
        except Exception as error:
            # TODO: el patrón Outbox resolvería esta ventana (guardado sin
            # TODO: publicar); se omite a propósito por alcance académico.
            raise EventPublishError() from error
        return saved
