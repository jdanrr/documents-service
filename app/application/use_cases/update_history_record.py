"""Caso de uso: actualizar registro del historial médico."""

from app.application.errors import EventPublishError, Forbidden, NotFound
from app.application.ports.input.use_cases import (
    UpdateMedicalHistoryRecordCommand,
    UpdateMedicalHistoryRecordUseCase,
)
from app.application.ports.output.event_publisher_port import EventPublisherPort
from app.application.ports.output.repository_ports import MedicalHistoryRecordRepository
from app.application.ports.output.system_ports import ClockPort
from app.domain import domain_events as events
from app.domain.entities import MedicalHistoryRecord
from app.domain.enums import DocumentOperation, DocumentType


class UpdateMedicalHistoryRecordUseCaseImpl(UpdateMedicalHistoryRecordUseCase):
    """Valida dueño, actualiza el registro y publica auditoría (UPDATE)."""

    def __init__(
        self,
        repository: MedicalHistoryRecordRepository,
        publisher: EventPublisherPort,
        clock: ClockPort,
    ) -> None:
        self._repository = repository
        self._publisher = publisher
        self._clock = clock

    async def execute(
        self, command: UpdateMedicalHistoryRecordCommand
    ) -> MedicalHistoryRecord:
        record = await self._repository.get_by_id(command.record_id)
        if record is None:
            raise NotFound("MedicalHistoryRecord", command.record_id)
        if record.user_id != command.user_id:
            raise Forbidden(command.record_id)
        record.update(command.category, command.description, self._clock.now())
        saved = await self._repository.update(record)
        outgoing = [
            events.DocumentsUpdated(
                document_id=saved.record_id,
                document_type=DocumentType.MEDICAL_HISTORY_RECORD,
                user_id=saved.user_id,
                operation=DocumentOperation.UPDATE,
                updated_at=saved.updated_at,
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
