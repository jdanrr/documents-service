"""Fake del generador de PDF (retorna bytes fijos)."""

from app.application.ports.output.pdf_storage_ports import PdfGeneratorPort
from app.domain.entities import AffiliationCertificate, MedicalHistoryRecord, ProfileSnapshot


class FakePdfGenerator(PdfGeneratorPort):
    """Retorna un PDF mínimo de mentiras."""

    async def generate_medical_history_pdf(
        self, user_id: str, records: list[MedicalHistoryRecord]
    ) -> bytes:
        return b"%PDF-1.4 fake medical history\n"

    async def generate_affiliation_certificate_pdf(
        self, snapshot: ProfileSnapshot, certificate: AffiliationCertificate
    ) -> bytes:
        return b"%PDF-1.4 fake certificate\n"
