"""Caso de uso: generar PDF del historial médico."""

from app.application.ports.input.use_cases import GenerateMedicalHistoryPdfUseCase
from app.application.ports.output.event_publisher_port import EventPublisherPort
from app.application.ports.output.pdf_storage_ports import (
    DocumentStoragePort,
    PdfGeneratorPort,
)
from app.application.ports.output.repository_ports import (
    MedicalHistoryExportRepository,
    MedicalHistoryRecordRepository,
)
from app.domain.entities import MedicalHistoryExport


class GenerateMedicalHistoryPdfUseCaseImpl(GenerateMedicalHistoryPdfUseCase):
    """Orquesta repositorios + PDF + storage + publicación del evento."""

    def __init__(
        self,
        record_repository: MedicalHistoryRecordRepository,
        export_repository: MedicalHistoryExportRepository,
        pdf_generator: PdfGeneratorPort,
        storage: DocumentStoragePort,
        publisher: EventPublisherPort,
    ) -> None:
        self._records = record_repository
        self._exports = export_repository
        self._pdf = pdf_generator
        self._storage = storage
        self._publisher = publisher

    async def execute(self, user_id: str, correlation_id: str) -> MedicalHistoryExport:
        # TODO: 1) listar registros con record_repository.list_by_user_id().
        # TODO: 2) generar bytes con pdf_generator.generate_medical_history_pdf().
        # TODO: 3) guardar binario con storage.save() (retorna referencia).
        # TODO: 4) crear y guardar entidad MedicalHistoryExport.
        # TODO: 5) publicar MedicalHistoryPdfGenerated + DocumentsUpdated (CREATE).
        raise NotImplementedError
