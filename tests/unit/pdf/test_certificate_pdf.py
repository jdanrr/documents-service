"""Tests del PDF del certificado (bytes válidos y contenido en español)."""

from datetime import datetime, timezone

import pytest

from app.domain.entities import AffiliationCertificate, ProfileSnapshot
from app.infrastructure.pdf.pdf_generator import ReportLabCertificatePdfGenerator

pytestmark = pytest.mark.unit


def _snapshot() -> ProfileSnapshot:
    """Titular de prueba."""
    return ProfileSnapshot(
        user_id="user-1",
        document_type="CC",
        document_number="1020304050",
        first_name="Maria Fernanda",
        last_name="Gomez Rojas",
        affiliation_start_date=datetime(2020, 6, 15, 12, 0, 0, tzinfo=timezone.utc),
    )


def _certificate() -> AffiliationCertificate:
    """Certificado de prueba (emitido 15/01/2026 12:00 UTC = 15/01/2026 en Bogotá)."""
    return AffiliationCertificate(
        cert_id="cert-1",
        user_id="user-1",
        affiliation_start_date=datetime(2020, 6, 15, 12, 0, 0, tzinfo=timezone.utc),
        issued_at=datetime(2026, 1, 15, 12, 0, 0, tzinfo=timezone.utc),
        file_key="certificates/user-1/cert-1.pdf",
    )


async def test_pdf_starts_with_magic_bytes():
    """El generador retorna bytes no vacíos que empiezan con %PDF."""
    content = await ReportLabCertificatePdfGenerator().generate_affiliation_certificate_pdf(
        _snapshot(), _certificate()
    )
    assert content.startswith(b"%PDF")
    assert len(content) > 100


async def test_pdf_contains_holder_data_and_dates():
    """El contenido incluye título, nombre, documento y fechas dd/mm/YYYY."""
    content = await ReportLabCertificatePdfGenerator().generate_affiliation_certificate_pdf(
        _snapshot(), _certificate()
    )
    text = content.decode("latin-1")
    # ReportLab escapa los acentos en el stream; se verifican tramos ASCII.
    assert "Certificado de afiliaci" in text
    assert "Maria Fernanda Gomez Rojas" in text
    assert "CC 1020304050" in text
    assert "15/06/2020" in text  # Afiliado desde (hora Colombia).
    assert "15/01/2026" in text  # Fecha de emisión (hora Colombia).
    assert "cert-1" in text
    assert "Documento generado autom" in text
    assert "fines acad" in text
