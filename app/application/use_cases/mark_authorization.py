"""Casos de uso: cambios de estado de entrega de autorizaciones (sin eventos)."""

from app.application.errors import NotFound
from app.application.ports.input.use_cases import (
    MarkAuthorizationCommand,
    MarkAuthorizationDeliveredUseCase,
    MarkAuthorizationDeliveryFailedUseCase,
)
from app.application.ports.output.repository_ports import AuthorizationRepository
from app.domain.entities import Authorization


class MarkAuthorizationDeliveredUseCaseImpl(MarkAuthorizationDeliveredUseCase):
    """Marca la autorización como enviada (ISSUED -> SENT)."""

    def __init__(self, repository: AuthorizationRepository) -> None:
        self._repository = repository

    async def execute(self, command: MarkAuthorizationCommand) -> Authorization:
        authorization = await self._repository.get_by_id(command.auth_id)
        if authorization is None:
            raise NotFound("Authorization", command.auth_id)
        authorization.mark_sent()
        return await self._repository.save(authorization)


class MarkAuthorizationDeliveryFailedUseCaseImpl(MarkAuthorizationDeliveryFailedUseCase):
    """Marca fallido el envío (ISSUED -> FAILED)."""

    def __init__(self, repository: AuthorizationRepository) -> None:
        self._repository = repository

    async def execute(self, command: MarkAuthorizationCommand) -> Authorization:
        authorization = await self._repository.get_by_id(command.auth_id)
        if authorization is None:
            raise NotFound("Authorization", command.auth_id)
        authorization.mark_failed()
        return await self._repository.save(authorization)
