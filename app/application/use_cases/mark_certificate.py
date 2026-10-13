"""Casos de uso: cambios de estado de entrega de certificados (sin eventos)."""

from app.application.errors import NotFound
from app.application.ports.input.use_cases import (
    MarkCertificateCommand,
    MarkCertificateDeliveredUseCase,
    MarkCertificateDeliveryFailedUseCase,
)
from app.application.ports.output.repository_ports import CertificateRepository
from app.domain.entities import AffiliationCertificate


class MarkCertificateDeliveredUseCaseImpl(MarkCertificateDeliveredUseCase):
    """Marca el certificado como enviado (ISSUED -> SENT)."""

    def __init__(self, repository: CertificateRepository) -> None:
        self._repository = repository

    async def execute(self, command: MarkCertificateCommand) -> AffiliationCertificate:
        certificate = await self._repository.get_by_id(command.cert_id)
        if certificate is None:
            raise NotFound("AffiliationCertificate", command.cert_id)
        certificate.mark_sent()
        return await self._repository.save(certificate)


class MarkCertificateDeliveryFailedUseCaseImpl(MarkCertificateDeliveryFailedUseCase):
    """Marca fallido el envío (ISSUED -> FAILED)."""

    def __init__(self, repository: CertificateRepository) -> None:
        self._repository = repository

    async def execute(self, command: MarkCertificateCommand) -> AffiliationCertificate:
        certificate = await self._repository.get_by_id(command.cert_id)
        if certificate is None:
            raise NotFound("AffiliationCertificate", command.cert_id)
        certificate.mark_failed()
        return await self._repository.save(certificate)
