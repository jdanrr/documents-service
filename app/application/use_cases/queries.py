"""Casos de uso de consulta (sin eventos)."""

from app.application.errors import NotFound
from app.application.ports.input.use_cases import (
    GetAffiliationCertificateCommand,
    GetAffiliationCertificateUseCase,
    GetAuthorizationCommand,
    GetAuthorizationUseCase,
    ListMedicalHistoryRecordsCommand,
    ListMedicalHistoryRecordsUseCase,
)
from app.application.ports.output.repository_ports import (
    AuthorizationRepository,
    CertificateRepository,
    MedicalHistoryRecordRepository,
)
from app.domain.entities import (
    AffiliationCertificate,
    Authorization,
    MedicalHistoryRecord,
)


class GetAuthorizationUseCaseImpl(GetAuthorizationUseCase):
    """Consulta una autorización por id."""

    def __init__(self, repository: AuthorizationRepository) -> None:
        self._repository = repository

    async def execute(self, command: GetAuthorizationCommand) -> Authorization:
        authorization = await self._repository.get_by_id(command.auth_id)
        if authorization is None:
            raise NotFound("Authorization", command.auth_id)
        return authorization


class GetAffiliationCertificateUseCaseImpl(GetAffiliationCertificateUseCase):
    """Consulta un certificado por id."""

    def __init__(self, repository: CertificateRepository) -> None:
        self._repository = repository

    async def execute(
        self, command: GetAffiliationCertificateCommand
    ) -> AffiliationCertificate:
        certificate = await self._repository.get_by_id(command.cert_id)
        if certificate is None:
            raise NotFound("AffiliationCertificate", command.cert_id)
        return certificate


class ListMedicalHistoryRecordsUseCaseImpl(ListMedicalHistoryRecordsUseCase):
    """Lista los registros del historial de un usuario."""

    def __init__(self, repository: MedicalHistoryRecordRepository) -> None:
        self._repository = repository

    async def execute(
        self, command: ListMedicalHistoryRecordsCommand
    ) -> list[MedicalHistoryRecord]:
        return await self._repository.list_by_user_id(command.user_id)
