"""Repositorios SQLAlchemy (esqueletos que cumplen los puertos de salida)."""

from sqlalchemy.orm import Session

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


class SqlAlchemyAuthorizationRepository(AuthorizationRepository):
    """Persiste autorizaciones en PostgreSQL."""

    def __init__(self, session: Session) -> None:
        self._session = session

    async def save(self, authorization: Authorization) -> Authorization:
        # TODO: mappers.authorization_to_orm + session.add/commit/refresh + to_domain.
        raise NotImplementedError

    async def get_by_id(self, auth_id: str) -> Authorization | None:
        # TODO: session.get(AuthorizationModel, auth_id) + to_domain o None.
        raise NotImplementedError

    async def list_by_user_id(self, user_id: str) -> list[Authorization]:
        # TODO: select por user_id ordenado por issued_at.
        raise NotImplementedError


class SqlAlchemyCertificateRepository(CertificateRepository):
    """Persiste certificados en PostgreSQL."""

    def __init__(self, session: Session) -> None:
        self._session = session

    async def save(self, certificate: AffiliationCertificate) -> AffiliationCertificate:
        # TODO: implementar como en autorizaciones.
        raise NotImplementedError

    async def get_by_id(self, cert_id: str) -> AffiliationCertificate | None:
        # TODO: implementar.
        raise NotImplementedError

    async def list_by_user_id(self, user_id: str) -> list[AffiliationCertificate]:
        # TODO: implementar.
        raise NotImplementedError


class SqlAlchemyMedicalHistoryRecordRepository(MedicalHistoryRecordRepository):
    """Persiste registros del historial en PostgreSQL."""

    def __init__(self, session: Session) -> None:
        self._session = session

    async def save(self, record: MedicalHistoryRecord) -> MedicalHistoryRecord:
        # TODO: implementar.
        raise NotImplementedError

    async def get_by_id(self, record_id: str) -> MedicalHistoryRecord | None:
        # TODO: implementar.
        raise NotImplementedError

    async def list_by_user_id(self, user_id: str) -> list[MedicalHistoryRecord]:
        # TODO: implementar.
        raise NotImplementedError

    async def update(self, record: MedicalHistoryRecord) -> MedicalHistoryRecord:
        # TODO: merge + commit; lanzar DocumentNotFoundError si falta.
        raise NotImplementedError


class SqlAlchemyMedicalHistoryExportRepository(MedicalHistoryExportRepository):
    """Persiste metadatos de exportaciones en PostgreSQL."""

    def __init__(self, session: Session) -> None:
        self._session = session

    async def save(self, export: MedicalHistoryExport) -> MedicalHistoryExport:
        # TODO: implementar.
        raise NotImplementedError

    async def get_by_id(self, pdf_id: str) -> MedicalHistoryExport | None:
        # TODO: implementar.
        raise NotImplementedError
