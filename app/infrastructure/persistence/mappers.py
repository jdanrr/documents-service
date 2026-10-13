"""Mappers modelo ORM <-> entidad de dominio (nunca exponer el ORM fuera del adaptador)."""

from app.domain.entities import (
    AffiliationCertificate,
    Authorization,
    MedicalHistoryExport,
    MedicalHistoryRecord,
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
    # TODO: mapear campos + DocumentStatus(row.status).
    raise NotImplementedError


def certificate_to_orm(entity: AffiliationCertificate) -> orm.AffiliationCertificateModel:
    """Dominio -> ORM."""
    # TODO: mapear campos + entity.status.value.
    raise NotImplementedError


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
