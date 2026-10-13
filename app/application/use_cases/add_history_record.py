"""Caso de uso: agregar registro al historial médico."""

from app.application.errors import EventPublishError
from app.application.ports.input.use_cases import (
    AddMedicalHistoryRecordCommand,
    AddMedicalHistoryRecordUseCase,
)
from app.application.ports.output.event_publisher_port import EventPublisherPort
from app.application.ports.output.repository_ports import MedicalHistoryRecordRepository
from app.application.ports.output.system_ports import ClockPort, IdGeneratorPort
from app.domain import domain_events as events
from app.domain.entities import MedicalHistoryRecord
from app.domain.enums import DocumentOperation, DocumentType


class AddMedicalHistoryRecordUseCaseImpl(AddMedicalHistoryRecordUseCase):
    """Crea el registro, lo guarda y publica solo auditoría (nada a Notifications)."""

    def __init__(
        self,
        repository: MedicalHistoryRecordRepository,
        publisher: EventPublisherPort,
        clock: ClockPort,
        ids: IdGeneratorPort,
    ) -> None:
        self._repository = repository
        self._publisher = publisher
        self._clock = clock
        self._ids = ids

    async def execute(
        self, command: AddMedicalHistoryRecordCommand
    ) -> MedicalHistoryRecord:
        now = self._clock.now()
        record = MedicalHistoryRecord(
            record_id=str(self._ids.new_id()),
            user_id=command.user_id,
            category=command.category,
            description=command.description,
            added_at=now,
            updated_at=now,
        )
        saved = await self._repository.save(record)
        outgoing = [
            events.DocumentsUpdated(
                document_id=saved.record_id,
                document_type=DocumentType.MEDICAL_HISTORY_RECORD,
                user_id=saved.user_id,
                operation=DocumentOperation.CREATE,
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
