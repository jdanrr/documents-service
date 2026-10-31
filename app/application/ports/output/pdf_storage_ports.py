"""Puertos de generación de PDF y almacenamiento de documentos."""

from abc import ABC, abstractmethod

from app.domain.entities import AffiliationCertificate, MedicalHistoryRecord, ProfileSnapshot


class PdfGeneratorPort(ABC):
    """Genera el binario del PDF (p. ej. autorización, certificado, historial)."""

    @abstractmethod
    async def generate_medical_history_pdf(
        self, user_id: str, records: list[MedicalHistoryRecord]
    ) -> bytes:
        """Genera el PDF del historial y retorna los bytes."""
        # TODO: implementar en infrastructure/pdf
        raise NotImplementedError

    @abstractmethod
    async def generate_affiliation_certificate_pdf(
        self, snapshot: ProfileSnapshot, certificate: AffiliationCertificate
    ) -> bytes:
        """Genera el PDF del certificado de afiliación y retorna los bytes."""
        raise NotImplementedError


class DocumentStoragePort(ABC):
    """Guarda binarios de documentos (PDFs) y retorna una referencia (key/URL)."""

    @abstractmethod
    async def save(
        self, key: str, content: bytes, content_type: str = "application/pdf"
    ) -> str:
        """Sube el binario con la key dada y retorna su referencia (p. ej. key de S3)."""
        # TODO: implementar en infrastructure/storage (S3)
        raise NotImplementedError
