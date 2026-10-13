"""Puertos de repositorios (una interfaz por entidad)."""

from abc import ABC, abstractmethod

from app.domain.entities import (
    AffiliationCertificate,
    Authorization,
    MedicalHistoryExport,
    MedicalHistoryRecord,
)


class AuthorizationRepository(ABC):
    """Persiste autorizaciones médicas."""

    @abstractmethod
    async def save(self, authorization: Authorization) -> Authorization:
        # TODO: implementar en infraestructura
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, auth_id: str) -> Authorization | None:
        # TODO: implementar en infraestructura
        raise NotImplementedError

    @abstractmethod
    async def list_by_user_id(self, user_id: str) -> list[Authorization]:
        # TODO: implementar en infraestructura
        raise NotImplementedError


class CertificateRepository(ABC):
    """Persiste certificados de afiliación."""

    @abstractmethod
    async def save(self, certificate: AffiliationCertificate) -> AffiliationCertificate:
        # TODO: implementar en infraestructura
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, cert_id: str) -> AffiliationCertificate | None:
        # TODO: implementar en infraestructura
        raise NotImplementedError

    @abstractmethod
    async def list_by_user_id(self, user_id: str) -> list[AffiliationCertificate]:
        # TODO: implementar en infraestructura
        raise NotImplementedError


class MedicalHistoryRecordRepository(ABC):
    """Persiste registros del historial médico."""

    @abstractmethod
    async def save(self, record: MedicalHistoryRecord) -> MedicalHistoryRecord:
        # TODO: implementar en infraestructura
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, record_id: str) -> MedicalHistoryRecord | None:
        # TODO: implementar en infraestructura
        raise NotImplementedError

    @abstractmethod
    async def list_by_user_id(self, user_id: str) -> list[MedicalHistoryRecord]:
        # TODO: implementar en infraestructura
        raise NotImplementedError

    @abstractmethod
    async def update(self, record: MedicalHistoryRecord) -> MedicalHistoryRecord:
        # TODO: implementar en infraestructura
        raise NotImplementedError


class MedicalHistoryExportRepository(ABC):
    """Persiste metadatos de exportaciones del historial a PDF."""

    @abstractmethod
    async def save(self, export: MedicalHistoryExport) -> MedicalHistoryExport:
        # TODO: implementar en infraestructura
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, pdf_id: str) -> MedicalHistoryExport | None:
        # TODO: implementar en infraestructura
        raise NotImplementedError
