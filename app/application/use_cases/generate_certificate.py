"""Caso de uso: generar certificado de afiliación."""

from app.application.errors import EventPublishError, ProfileNotFound, StorageError
from app.application.ports.input.use_cases import (
    GenerateAffiliationCertificateCommand,
    GenerateAffiliationCertificateUseCase,
)
from app.application.ports.output.event_publisher_port import EventPublisherPort
from app.application.ports.output.pdf_storage_ports import (
    DocumentStoragePort,
    PdfGeneratorPort,
)
from app.application.ports.output.repository_ports import (
    CertificateRepository,
    ProfileSnapshotRepository,
)
from app.application.ports.output.system_ports import ClockPort, IdGeneratorPort
from app.domain import domain_events as events
from app.domain.entities import AffiliationCertificate


class GenerateAffiliationCertificateUseCaseImpl(GenerateAffiliationCertificateUseCase):
    """Genera el PDF, lo sube, guarda el certificado y publica su evento.

    Orden: PDF -> S3 -> BD -> bus. Si falla la subida no se guarda ni se
    publica nada; si falla la publicación, lo guardado NO se revierte.
    """

    def __init__(
        self,
        snapshots: ProfileSnapshotRepository,
        certificates: CertificateRepository,
        pdf_generator: PdfGeneratorPort,
        storage: DocumentStoragePort,
        publisher: EventPublisherPort,
        clock: ClockPort,
        ids: IdGeneratorPort,
    ) -> None:
        self._snapshots = snapshots
        self._certificates = certificates
        self._pdf = pdf_generator
        self._storage = storage
        self._publisher = publisher
        self._clock = clock
        self._ids = ids

    async def execute(
        self, command: GenerateAffiliationCertificateCommand
    ) -> AffiliationCertificate:
        snapshot = await self._snapshots.get_by_user_id(command.user_id)
        if snapshot is None:
            raise ProfileNotFound(command.user_id)
        now = self._clock.now()
        certificate = AffiliationCertificate(
            cert_id=str(self._ids.new_id()),
            user_id=command.user_id,
            affiliation_start_date=snapshot.affiliation_start_date,
            issued_at=now,
        )
        content = await self._pdf.generate_affiliation_certificate_pdf(
            snapshot, certificate
        )
        file_key = f"certificates/{command.user_id}/{certificate.cert_id}.pdf"
        certificate.file_key = file_key
        try:
            await self._storage.save(file_key, content)
        except StorageError:
            raise
        except Exception as error:
            raise StorageError("No se pudo guardar el PDF del certificado.") from error
        saved = await self._certificates.save(certificate)
        outgoing = [
            events.CertificateGenerated(
                cert_id=saved.cert_id,
                user_id=saved.user_id,
                email=command.email,
                first_name=command.first_name,
                issued_at=saved.issued_at,
                file_key=saved.file_key,
                file_name=f"certificado-afiliacion-{saved.cert_id}.pdf",
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
