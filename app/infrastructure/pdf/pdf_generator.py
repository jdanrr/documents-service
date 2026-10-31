"""Adaptador generador de PDF (ReportLab para certificados; historial pendiente)."""

from datetime import datetime, timedelta, timezone
from io import BytesIO

from reportlab.pdfgen import canvas

from app.application.ports.output.pdf_storage_ports import PdfGeneratorPort
from app.domain.entities import AffiliationCertificate, MedicalHistoryRecord, ProfileSnapshot

# Colombia no tiene horario de verano: UTC-5 fijo (evita depender de tzdata).
COLOMBIA_TZ = timezone(timedelta(hours=-5))

FOOTER = "Documento generado automáticamente. Datos ficticios con fines académicos."


def _format_co_date(moment: datetime) -> str:
    """Formatea un instante en dd/mm/YYYY con hora de Colombia."""
    return moment.astimezone(COLOMBIA_TZ).strftime("%d/%m/%Y")


class StubPdfGenerator(PdfGeneratorPort):
    """Generador de mentiras para arrancar sin dependencia PDF real."""

    async def generate_medical_history_pdf(
        self, user_id: str, records: list[MedicalHistoryRecord]
    ) -> bytes:
        # TODO: elegir librería (reportlab/fpdf) y generar el binario real.
        # TODO: por ahora retornar b"" o un PDF mínimo de prueba.
        raise NotImplementedError

    async def generate_affiliation_certificate_pdf(
        self, snapshot: ProfileSnapshot, certificate: AffiliationCertificate
    ) -> bytes:
        raise NotImplementedError


class ReportLabCertificatePdfGenerator(PdfGeneratorPort):
    """Genera el PDF del certificado de afiliación con ReportLab."""

    async def generate_medical_history_pdf(
        self, user_id: str, records: list[MedicalHistoryRecord]
    ) -> bytes:
        # El historial es otro feature: no se implementa aquí.
        raise NotImplementedError

    async def generate_affiliation_certificate_pdf(
        self, snapshot: ProfileSnapshot, certificate: AffiliationCertificate
    ) -> bytes:
        buffer = BytesIO()
        # Sin compresión: el texto queda legible en los bytes (verificable en tests).
        pdf = canvas.Canvas(buffer, pageCompression=0)
        pdf.setTitle("Certificado de afiliación")
        y = 750
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(72, y, "Certificado de afiliación")
        y -= 40
        pdf.setFont("Helvetica", 12)
        lines = [
            f"Nombre: {snapshot.full_name}",
            f"Documento: {snapshot.document_type} {snapshot.document_number}",
            f"Afiliado desde: {_format_co_date(certificate.affiliation_start_date)}",
            f"Fecha de emisión: {_format_co_date(certificate.issued_at)}",
            f"Certificado: {certificate.cert_id}",
            "",
            FOOTER,
        ]
        for line in lines:
            pdf.drawString(72, y, line)
            y -= 20
        pdf.showPage()
        pdf.save()
        return buffer.getvalue()
