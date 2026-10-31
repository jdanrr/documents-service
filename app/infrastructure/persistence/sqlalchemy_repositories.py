"""Repositorios SQLAlchemy (implementados: certificado y snapshot; resto esqueleto)."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application.ports.output.repository_ports import (
    AuthorizationRepository,
    CertificateRepository,
    MedicalHistoryExportRepository,
    MedicalHistoryRecordRepository,
    ProfileSnapshotRepository,
)
from app.domain.entities import (
    AffiliationCertificate,
    Authorization,
    MedicalHistoryExport,
    MedicalHistoryRecord,
    ProfileSnapshot,
)
from app.infrastructure.persistence import mappers
from app.infrastructure.persistence.models import (
    AffiliationCertificateModel,
    ProfileSnapshotModel,
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
        row = mappers.certificate_to_orm(certificate)
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return mappers.certificate_to_domain(row)

    async def get_by_id(self, cert_id: str) -> AffiliationCertificate | None:
        row = self._session.get(AffiliationCertificateModel, cert_id)
        return mappers.certificate_to_domain(row) if row is not None else None

    async def list_by_user_id(self, user_id: str) -> list[AffiliationCertificate]:
        rows = self._session.scalars(
            select(AffiliationCertificateModel)
            .where(AffiliationCertificateModel.user_id == user_id)
            .order_by(AffiliationCertificateModel.issued_at)
        ).all()
        return [mappers.certificate_to_domain(row) for row in rows]


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


class SqlAlchemyProfileSnapshotRepository(ProfileSnapshotRepository):
    """Lee la copia mínima del titular en PostgreSQL."""

    def __init__(self, session: Session) -> None:
        self._session = session

    async def get_by_user_id(self, user_id: str) -> ProfileSnapshot | None:
        row = self._session.get(ProfileSnapshotModel, user_id)
        return mappers.snapshot_to_domain(row) if row is not None else None
