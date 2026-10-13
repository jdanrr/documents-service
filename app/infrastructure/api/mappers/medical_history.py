"""Mappers de historial médico: schema <-> dominio <-> evento."""

from app.domain import domain_events as events
from app.domain.entities import MedicalHistoryExport, MedicalHistoryRecord


def record_to_response(entity: MedicalHistoryRecord) -> dict:
    """Convierte registro a dict de respuesta."""
    # TODO: mapear record_id -> recordId, added_at/updated_at, etc.
    raise NotImplementedError


def export_to_response(entity: MedicalHistoryExport) -> dict:
    """Convierte exportación a dict de respuesta."""
    # TODO: mapear pdf_id -> pdfId, record_count -> recordCount, etc.
    raise NotImplementedError


def export_to_domain_event(
    entity: MedicalHistoryExport, correlation_id: str
) -> events.MedicalHistoryPdfGenerated:
    """Convierte exportación a evento de dominio."""
    # TODO: construir MedicalHistoryPdfGenerated.
    raise NotImplementedError
