"""Repositorios en memoria para desarrollo local (esqueleto).

TODO: sustituir por DynamoDB/RDS sin cambiar los puertos.
"""

from app.application.ports.output.repository_ports import (
    AuthorizationRepository,
    CertificateRepository,
    MedicalHistoryExportRepository,
    MedicalHistoryRecordRepository,
)
from app.domain.entities import (
    AffiliationCertificate,
    Authorization,
    MedicalHistoryExport,
    MedicalHistoryRecord,
)


class InMemoryAuthorizationRepository(AuthorizationRepository):
    """Guarda autorizaciones en un dict (solo para arrancar sin DB real)."""

    def __init__(self) -> None:
        self._store: dict[str, Authorization] = {}

    async def save(self, authorization: Authorization) -> Authorization:
        # TODO: self._store[authorization.auth_id] = authorization
        raise NotImplementedError

    async def get_by_id(self, auth_id: str) -> Authorization | None:
        # TODO: return self._store.get(auth_id)
        raise NotImplementedError

    async def list_by_user_id(self, user_id: str) -> list[Authorization]:
        # TODO: filtrar por user_id
        raise NotImplementedError


class InMemoryCertificateRepository(CertificateRepository):
    """Guarda certificados en un dict."""

    def __init__(self) -> None:
        self._store: dict[str, AffiliationCertificate] = {}

    async def save(self, certificate: AffiliationCertificate) -> AffiliationCertificate:
        # TODO: implementar
        raise NotImplementedError

    async def get_by_id(self, cert_id: str) -> AffiliationCertificate | None:
        # TODO: implementar
        raise NotImplementedError

    async def list_by_user_id(self, user_id: str) -> list[AffiliationCertificate]:
        # TODO: implementar
        raise NotImplementedError


class InMemoryMedicalHistoryRecordRepository(MedicalHistoryRecordRepository):
    """Guarda registros del historial en un dict."""

    def __init__(self) -> None:
        self._store: dict[str, MedicalHistoryRecord] = {}

    async def save(self, record: MedicalHistoryRecord) -> MedicalHistoryRecord:
        # TODO: implementar
        raise NotImplementedError

    async def get_by_id(self, record_id: str) -> MedicalHistoryRecord | None:
        # TODO: implementar
        raise NotImplementedError

    async def list_by_user_id(self, user_id: str) -> list[MedicalHistoryRecord]:
        # TODO: implementar
        raise NotImplementedError

    async def update(self, record: MedicalHistoryRecord) -> MedicalHistoryRecord:
        # TODO: implementar (lanzar DocumentNotFoundError si falta)
        raise NotImplementedError


class InMemoryMedicalHistoryExportRepository(MedicalHistoryExportRepository):
    """Guarda metadatos de exportaciones en un dict."""

    def __init__(self) -> None:
        self._store: dict[str, MedicalHistoryExport] = {}

    async def save(self, export: MedicalHistoryExport) -> MedicalHistoryExport:
        # TODO: implementar
        raise NotImplementedError

    async def get_by_id(self, pdf_id: str) -> MedicalHistoryExport | None:
        # TODO: implementar
        raise NotImplementedError
