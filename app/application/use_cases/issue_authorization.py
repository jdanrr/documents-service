"""Caso de uso: emitir autorización médica."""

from app.application.ports.input.use_cases import IssueAuthorizationUseCase
from app.application.ports.output.event_publisher_port import EventPublisherPort
from app.application.ports.output.repository_ports import AuthorizationRepository
from app.domain.entities import Authorization


class IssueAuthorizationUseCaseImpl(IssueAuthorizationUseCase):
    """Orquesta dominio + puertos para emitir una autorización."""

    def __init__(
        self,
        repository: AuthorizationRepository,
        publisher: EventPublisherPort,
    ) -> None:
        self._repository = repository
        self._publisher = publisher

    async def execute(
        self,
        user_id: str,
        procedure: str,
        doctor: str,
        location: str,
        correlation_id: str,
    ) -> Authorization:
        # TODO: 1) crear entidad Authorization (uuid + now UTC + ISSUED).
        # TODO: 2) guardar con repository.save().
        # TODO: 3) mapear a evento de dominio AuthorizationIssued.
        # TODO: 4) publicar con publisher.publish_authorization_issued().
        # TODO: 5) publicar DocumentsUpdated (CREATE) para auditoría.
        raise NotImplementedError
