"""Mappers modelo ORM <-> entidad de dominio (nunca exponer el ORM fuera del adaptador)."""

from app.domain.entities import (
    AffiliationCertificate,
    Authorization,
    MedicalHistoryExport,
    MedicalHistoryRecord,
    ProfileSnapshot,
)
from app.domain.enums import DocumentStatus
from app.infrastructure.persistence import models as orm


def authorization_to_domain(row: orm.AuthorizationModel) -> Authorization:
    """ORM -> dominio."""
    # TODO: mapear campos + DocumentStatus(row.status).
    raise NotImplementedError


def authorization_to_orm(entity: Authorization) -> orm.AuthorizationModel:
    """Dominio -> ORM."""
    # TODO: mapear campos + entity.status.value.
    raise NotImplementedError


def certificate_to_domain(row: orm.AffiliationCertificateModel) -> AffiliationCertificate:
    """ORM -> dominio."""
    return AffiliationCertificate(
        cert_id=row.cert_id,
        user_id=row.user_id,
        affiliation_start_date=row.affiliation_start_date,
        issued_at=row.issued_at,
        file_key=row.file_key,
        status=DocumentStatus(row.status),
    )


def certificate_to_orm(entity: AffiliationCertificate) -> orm.AffiliationCertificateModel:
    """Dominio -> ORM."""
    return orm.AffiliationCertificateModel(
        cert_id=entity.cert_id,
        user_id=entity.user_id,
        affiliation_start_date=entity.affiliation_start_date,
        issued_at=entity.issued_at,
        file_key=entity.file_key,
        status=entity.status.value,
    )


def snapshot_to_domain(row: orm.ProfileSnapshotModel) -> ProfileSnapshot:
    """ORM -> dominio."""
    return ProfileSnapshot(
        user_id=row.user_id,
        document_type=row.document_type,
        document_number=row.document_number,
        first_name=row.first_name,
        last_name=row.last_name,
        affiliation_start_date=row.affiliation_start_date,
    )


def snapshot_to_orm(entity: ProfileSnapshot) -> orm.ProfileSnapshotModel:
    """Dominio -> ORM."""
    return orm.ProfileSnapshotModel(
        user_id=entity.user_id,
        document_type=entity.document_type,
        document_number=entity.document_number,
        first_name=entity.first_name,
        last_name=entity.last_name,
        affiliation_start_date=entity.affiliation_start_date,
    )


def record_to_domain(row: orm.MedicalHistoryRecordModel) -> MedicalHistoryRecord:
    """ORM -> dominio."""
    # TODO: mapear campos.
    raise NotImplementedError


def record_to_orm(entity: MedicalHistoryRecord) -> orm.MedicalHistoryRecordModel:
    """Dominio -> ORM."""
    # TODO: mapear campos.
    raise NotImplementedError


def export_to_domain(row: orm.MedicalHistoryExportModel) -> MedicalHistoryExport:
    """ORM -> dominio."""
    # TODO: mapear campos.
    raise NotImplementedError


def export_to_orm(entity: MedicalHistoryExport) -> orm.MedicalHistoryExportModel:
    """Dominio -> ORM."""
    # TODO: mapear campos.
    raise NotImplementedError
