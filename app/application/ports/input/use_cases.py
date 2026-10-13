"""Puertos de entrada: un caso de uso por acción de negocio."""

from abc import ABC, abstractmethod

from app.domain.entities import (
    AffiliationCertificate,
    Authorization,
    MedicalHistoryExport,
    MedicalHistoryRecord,
)


class IssueAuthorizationUseCase(ABC):
    """Emite una autorización médica."""

    @abstractmethod
    async def execute(
        self,
        user_id: str,
        procedure: str,
        doctor: str,
        location: str,
        correlation_id: str,
    ) -> Authorization:
        """Crea la autorización, la persiste y publica AuthorizationIssued."""
        # TODO: implementar en use_cases/issue_authorization.py
        raise NotImplementedError


class GenerateAffiliationCertificateUseCase(ABC):
    """Genera el certificado de afiliación."""

    @abstractmethod
    async def execute(self, user_id: str, correlation_id: str) -> AffiliationCertificate:
        """Crea el certificado, lo persiste y publica CertificateGenerated."""
        # TODO: implementar en use_cases/generate_certificate.py
        raise NotImplementedError


class AddMedicalHistoryRecordUseCase(ABC):
    """Agrega un registro al historial médico."""

    @abstractmethod
    async def execute(
        self,
        user_id: str,
        category: str,
        description: str,
        correlation_id: str,
    ) -> MedicalHistoryRecord:
        """Crea el registro, lo persiste y publica DocumentsUpdated (CREATE)."""
        # TODO: implementar en use_cases/add_history_record.py
        raise NotImplementedError


class UpdateMedicalHistoryRecordUseCase(ABC):
    """Actualiza un registro del historial médico."""

    @abstractmethod
    async def execute(
        self,
        record_id: str,
        category: str,
        description: str,
        correlation_id: str,
    ) -> MedicalHistoryRecord:
        """Actualiza el registro y publica DocumentsUpdated (UPDATE)."""
        # TODO: implementar en use_cases/update_history_record.py
        raise NotImplementedError


class GenerateMedicalHistoryPdfUseCase(ABC):
    """Genera el PDF del historial médico."""

    @abstractmethod
    async def execute(self, user_id: str, correlation_id: str) -> MedicalHistoryExport:
        """Genera el PDF, lo guarda en storage y publica MedicalHistoryPdfGenerated."""
        # TODO: implementar en use_cases/generate_history_pdf.py
        raise NotImplementedError
