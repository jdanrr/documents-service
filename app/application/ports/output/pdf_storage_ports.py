"""Puertos de generación de PDF y almacenamiento de documentos."""

from abc import ABC, abstractmethod

from app.domain.entities import MedicalHistoryRecord


class PdfGeneratorPort(ABC):
    """Genera el binario del PDF (p. ej. autorización, certificado, historial)."""

    @abstractmethod
    async def generate_medical_history_pdf(
        self, user_id: str, records: list[MedicalHistoryRecord]
    ) -> bytes:
        """Genera el PDF del historial y retorna los bytes."""
        # TODO: implementar en infrastructure/pdf
        raise NotImplementedError


class DocumentStoragePort(ABC):
    """Guarda binarios de documentos (PDFs) y retorna una referencia (key/URL)."""

    @abstractmethod
    async def save(self, pdf_id: str, content: bytes) -> str:
        """Guarda el PDF y retorna su referencia (p. ej. key de S3)."""
        # TODO: implementar en infrastructure/storage (S3)
        raise NotImplementedError
