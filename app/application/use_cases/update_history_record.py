"""Caso de uso: actualizar registro del historial médico."""

from app.application.ports.input.use_cases import UpdateMedicalHistoryRecordUseCase
from app.application.ports.output.event_publisher_port import EventPublisherPort
from app.application.ports.output.repository_ports import MedicalHistoryRecordRepository
from app.domain.entities import MedicalHistoryRecord
from app.domain.exceptions import DocumentNotFoundError


class UpdateMedicalHistoryRecordUseCaseImpl(UpdateMedicalHistoryRecordUseCase):
    """Orquesta dominio + puertos para actualizar un registro."""

    def __init__(
        self,
        repository: MedicalHistoryRecordRepository,
        publisher: EventPublisherPort,
    ) -> None:
        self._repository = repository
        self._publisher = publisher

    async def execute(
        self,
        record_id: str,
        category: str,
        description: str,
        correlation_id: str,
    ) -> MedicalHistoryRecord:
        # TODO: 1) buscar con repository.get_by_id(); si falta, lanzar DocumentNotFoundError.
        # TODO: 2) actualizar campos + updated_at UTC.
        # TODO: 3) guardar con repository.update().
        # TODO: 4) publicar DocumentsUpdated (UPDATE).
        raise NotImplementedError
