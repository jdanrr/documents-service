"""Repositorios falsos en memoria (cumplen los puertos para tests)."""

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
    """Fake de autorizaciones (dict)."""

    def __init__(self) -> None:
        self.items: dict[str, Authorization] = {}

    async def save(self, authorization: Authorization) -> Authorization:
        self.items[authorization.auth_id] = authorization
        return authorization

    async def get_by_id(self, auth_id: str) -> Authorization | None:
        return self.items.get(auth_id)

    async def list_by_user_id(self, user_id: str) -> list[Authorization]:
        return [a for a in self.items.values() if a.user_id == user_id]


class InMemoryCertificateRepository(CertificateRepository):
    """Fake de certificados (dict)."""

    def __init__(self) -> None:
        self.items: dict[str, AffiliationCertificate] = {}

    async def save(self, certificate: AffiliationCertificate) -> AffiliationCertificate:
        self.items[certificate.cert_id] = certificate
        return certificate

    async def get_by_id(self, cert_id: str) -> AffiliationCertificate | None:
        return self.items.get(cert_id)

    async def list_by_user_id(self, user_id: str) -> list[AffiliationCertificate]:
        return [c for c in self.items.values() if c.user_id == user_id]


class InMemoryMedicalHistoryRecordRepository(MedicalHistoryRecordRepository):
    """Fake de registros del historial (dict)."""

    def __init__(self) -> None:
        self.items: dict[str, MedicalHistoryRecord] = {}

    async def save(self, record: MedicalHistoryRecord) -> MedicalHistoryRecord:
        self.items[record.record_id] = record
        return record

    async def get_by_id(self, record_id: str) -> MedicalHistoryRecord | None:
        return self.items.get(record_id)

    async def list_by_user_id(self, user_id: str) -> list[MedicalHistoryRecord]:
        return [r for r in self.items.values() if r.user_id == user_id]

    async def update(self, record: MedicalHistoryRecord) -> MedicalHistoryRecord:
        self.items[record.record_id] = record
        return record


class InMemoryMedicalHistoryExportRepository(MedicalHistoryExportRepository):
    """Fake de exportaciones (dict)."""

    def __init__(self) -> None:
        self.items: dict[str, MedicalHistoryExport] = {}

    async def save(self, export: MedicalHistoryExport) -> MedicalHistoryExport:
        self.items[export.pdf_id] = export
        return export

    async def get_by_id(self, pdf_id: str) -> MedicalHistoryExport | None:
        return self.items.get(pdf_id)
