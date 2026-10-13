"""Adaptador generador de PDF (esqueleto, sin librería real por ahora)."""

from app.application.ports.output.pdf_storage_ports import PdfGeneratorPort
from app.domain.entities import MedicalHistoryRecord


class StubPdfGenerator(PdfGeneratorPort):
    """Generador de mentiras para arrancar sin dependencia PDF real."""

    async def generate_medical_history_pdf(
        self, user_id: str, records: list[MedicalHistoryRecord]
    ) -> bytes:
        # TODO: elegir librería (reportlab/fpdf) y generar el binario real.
        # TODO: por ahora retornar b"" o un PDF mínimo de prueba.
        raise NotImplementedError
