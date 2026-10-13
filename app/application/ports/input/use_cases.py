"""Puertos de entrada: un caso de uso por acción, con execute(command) -> result.

Comandos y resultados como dataclass(frozen=True), solo librería estándar.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.domain.entities import (
    AffiliationCertificate,
    Authorization,
    MedicalHistoryExport,
    MedicalHistoryRecord,
)


@dataclass(frozen=True)
class IssueAuthorizationCommand:
    """Comando para emitir una autorización médica."""

    user_id: str
    procedure: str
    doctor: str
    location: str
    correlation_id: str


class IssueAuthorizationUseCase(ABC):
    """Emite una autorización médica."""

    @abstractmethod
    async def execute(self, command: IssueAuthorizationCommand) -> Authorization:
        """Crea la autorización, la persiste y publica sus eventos."""
        raise NotImplementedError


@dataclass(frozen=True)
class GenerateAffiliationCertificateCommand:
    """Comando para generar el certificado de afiliación."""

    user_id: str
    correlation_id: str


class GenerateAffiliationCertificateUseCase(ABC):
    """Genera el certificado de afiliación."""

    @abstractmethod
    async def execute(
        self, command: GenerateAffiliationCertificateCommand
    ) -> AffiliationCertificate:
        """Crea el certificado, lo persiste y publica sus eventos."""
        raise NotImplementedError


@dataclass(frozen=True)
class AddMedicalHistoryRecordCommand:
    """Comando para agregar un registro al historial."""

    user_id: str
    category: str
    description: str
    correlation_id: str


class AddMedicalHistoryRecordUseCase(ABC):
    """Agrega un registro al historial médico."""

    @abstractmethod
    async def execute(
        self, command: AddMedicalHistoryRecordCommand
    ) -> MedicalHistoryRecord:
        """Crea el registro, lo persiste y publica DocumentsUpdated (CREATE)."""
        raise NotImplementedError


@dataclass(frozen=True)
class UpdateMedicalHistoryRecordCommand:
    """Comando para actualizar un registro del historial."""

    record_id: str
    user_id: str
    category: str
    description: str
    correlation_id: str


class UpdateMedicalHistoryRecordUseCase(ABC):
    """Actualiza un registro del historial médico."""

    @abstractmethod
    async def execute(
        self, command: UpdateMedicalHistoryRecordCommand
    ) -> MedicalHistoryRecord:
        """Actualiza el registro y publica DocumentsUpdated (UPDATE)."""
        raise NotImplementedError


@dataclass(frozen=True)
class ExportMedicalHistoryPdfCommand:
    """Comando para exportar el historial a PDF."""

    user_id: str
    correlation_id: str


class ExportMedicalHistoryPdfUseCase(ABC):
    """Genera el PDF del historial médico."""

    @abstractmethod
    async def execute(
        self, command: ExportMedicalHistoryPdfCommand
    ) -> MedicalHistoryExport:
        """Genera el PDF, lo guarda y publica MedicalHistoryPdfGenerated."""
        raise NotImplementedError


@dataclass(frozen=True)
class MarkAuthorizationCommand:
    """Comando para cambiar el estado de entrega (sin eventos, sin correlation_id)."""

    auth_id: str


class MarkAuthorizationDeliveredUseCase(ABC):
    """Marca la autorización como enviada (ISSUED -> SENT)."""

    @abstractmethod
    async def execute(self, command: MarkAuthorizationCommand) -> Authorization:
        raise NotImplementedError


class MarkAuthorizationDeliveryFailedUseCase(ABC):
    """Marca fallido el envío (ISSUED -> FAILED)."""

    @abstractmethod
    async def execute(self, command: MarkAuthorizationCommand) -> Authorization:
        raise NotImplementedError


@dataclass(frozen=True)
class MarkCertificateCommand:
    """Comando para cambiar el estado de entrega (sin eventos, sin correlation_id)."""

    cert_id: str


class MarkCertificateDeliveredUseCase(ABC):
    """Marca el certificado como enviado (ISSUED -> SENT)."""

    @abstractmethod
    async def execute(
        self, command: MarkCertificateCommand
    ) -> AffiliationCertificate:
        raise NotImplementedError


class MarkCertificateDeliveryFailedUseCase(ABC):
    """Marca fallido el envío (ISSUED -> FAILED)."""

    @abstractmethod
    async def execute(
        self, command: MarkCertificateCommand
    ) -> AffiliationCertificate:
        raise NotImplementedError


@dataclass(frozen=True)
class GetAuthorizationCommand:
    """Comando para consultar una autorización."""

    auth_id: str


class GetAuthorizationUseCase(ABC):
    """Consulta una autorización por id."""

    @abstractmethod
    async def execute(self, command: GetAuthorizationCommand) -> Authorization:
        raise NotImplementedError


@dataclass(frozen=True)
class GetAffiliationCertificateCommand:
    """Comando para consultar un certificado."""

    cert_id: str


class GetAffiliationCertificateUseCase(ABC):
    """Consulta un certificado por id."""

    @abstractmethod
    async def execute(
        self, command: GetAffiliationCertificateCommand
    ) -> AffiliationCertificate:
        raise NotImplementedError


@dataclass(frozen=True)
class ListMedicalHistoryRecordsCommand:
    """Comando para listar el historial de un usuario."""

    user_id: str


class ListMedicalHistoryRecordsUseCase(ABC):
    """Lista los registros del historial de un usuario."""

    @abstractmethod
    async def execute(
        self, command: ListMedicalHistoryRecordsCommand
    ) -> list[MedicalHistoryRecord]:
        raise NotImplementedError
