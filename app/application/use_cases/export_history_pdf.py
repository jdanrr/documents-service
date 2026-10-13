"""Caso de uso: exportar el historial médico a PDF."""

from app.application.errors import EmptyMedicalHistory, EventPublishError
from app.application.ports.input.use_cases import (
    ExportMedicalHistoryPdfCommand,
    ExportMedicalHistoryPdfUseCase,
)
from app.application.ports.output.event_publisher_port import EventPublisherPort
from app.application.ports.output.pdf_storage_ports import (
    DocumentStoragePort,
    PdfGeneratorPort,
)
from app.application.ports.output.repository_ports import (
    MedicalHistoryExportRepository,
    MedicalHistoryRecordRepository,
)
from app.application.ports.output.system_ports import ClockPort, IdGeneratorPort
from app.domain import domain_events as events
from app.domain.entities import MedicalHistoryExport


class ExportMedicalHistoryPdfUseCaseImpl(ExportMedicalHistoryPdfUseCase):
    """Genera el PDF, lo guarda, registra la exportación y publica su evento."""

    def __init__(
        self,
        record_repository: MedicalHistoryRecordRepository,
        export_repository: MedicalHistoryExportRepository,
        pdf_generator: PdfGeneratorPort,
        storage: DocumentStoragePort,
        publisher: EventPublisherPort,
        clock: ClockPort,
        ids: IdGeneratorPort,
    ) -> None:
        self._records = record_repository
        self._exports = export_repository
        self._pdf = pdf_generator
        self._storage = storage
        self._publisher = publisher
        self._clock = clock
        self._ids = ids

    async def execute(
        self, command: ExportMedicalHistoryPdfCommand
    ) -> MedicalHistoryExport:
        records = await self._records.list_by_user_id(command.user_id)
        if not records:
            raise EmptyMedicalHistory(command.user_id)
        content = await self._pdf.generate_medical_history_pdf(command.user_id, records)
        pdf_id = str(self._ids.new_id())
        await self._storage.save(pdf_id, content)
        export = MedicalHistoryExport(
            pdf_id=pdf_id,
            user_id=command.user_id,
            record_count=len(records),
            generated_at=self._clock.now(),
        )
        saved = await self._exports.save(export)
        outgoing = [
            events.MedicalHistoryPdfGenerated(
                pdf_id=saved.pdf_id,
                user_id=saved.user_id,
                record_count=saved.record_count,
                generated_at=saved.generated_at,
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
