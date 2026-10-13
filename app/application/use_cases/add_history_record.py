"""Caso de uso: agregar registro al historial médico."""

from app.application.ports.input.use_cases import AddMedicalHistoryRecordUseCase
from app.application.ports.output.event_publisher_port import EventPublisherPort
from app.application.ports.output.repository_ports import MedicalHistoryRecordRepository
from app.domain.entities import MedicalHistoryRecord


class AddMedicalHistoryRecordUseCaseImpl(AddMedicalHistoryRecordUseCase):
    """Orquesta dominio + puertos para agregar un registro."""

    def __init__(
        self,
        repository: MedicalHistoryRecordRepository,
        publisher: EventPublisherPort,
    ) -> None:
        self._repository = repository
        self._publisher = publisher

    async def execute(
        self,
        user_id: str,
        category: str,
        description: str,
        correlation_id: str,
    ) -> MedicalHistoryRecord:
        # TODO: 1) crear entidad MedicalHistoryRecord (uuid + added_at/updated_at UTC).
        # TODO: 2) guardar con repository.save().
        # TODO: 3) mapear a evento DocumentsUpdated (CREATE).
        # TODO: 4) publicar con publisher.publish_documents_updated().
        raise NotImplementedError
