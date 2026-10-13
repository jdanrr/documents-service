"""Caso de uso: emitir autorización médica."""

from app.application.errors import EventPublishError
from app.application.ports.input.use_cases import (
    IssueAuthorizationCommand,
    IssueAuthorizationUseCase,
)
from app.application.ports.output.event_publisher_port import EventPublisherPort
from app.application.ports.output.repository_ports import AuthorizationRepository
from app.application.ports.output.system_ports import ClockPort, IdGeneratorPort
from app.domain import domain_events as events
from app.domain.entities import Authorization
from app.domain.enums import DocumentOperation, DocumentType


class IssueAuthorizationUseCaseImpl(IssueAuthorizationUseCase):
    """Crea la autorización con ISSUED, la guarda y publica sus eventos."""

    def __init__(
        self,
        repository: AuthorizationRepository,
        publisher: EventPublisherPort,
        clock: ClockPort,
        ids: IdGeneratorPort,
    ) -> None:
        self._repository = repository
        self._publisher = publisher
        self._clock = clock
        self._ids = ids

    async def execute(self, command: IssueAuthorizationCommand) -> Authorization:
        now = self._clock.now()
        authorization = Authorization(
            auth_id=str(self._ids.new_id()),
            user_id=command.user_id,
            procedure=command.procedure,
            doctor=command.doctor,
            location=command.location,
            issued_at=now,
        )
        # Orden: guardar primero, publicar después (sin UoW: un solo agregado).
        saved = await self._repository.save(authorization)
        outgoing = [
            events.AuthorizationIssued(
                auth_id=saved.auth_id,
                user_id=saved.user_id,
                procedure=saved.procedure,
                doctor=saved.doctor,
                location=saved.location,
                issued_at=saved.issued_at,
            ),
            events.DocumentsUpdated(
                document_id=saved.auth_id,
                document_type=DocumentType.AUTHORIZATION,
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
