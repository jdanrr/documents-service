"""Tests de ExportMedicalHistoryPdf (feliz, vacío y fallos)."""

import pytest

from app.application.errors import EmptyMedicalHistory, EventPublishError
from app.application.ports.input.use_cases import (
    AddMedicalHistoryRecordCommand,
    ExportMedicalHistoryPdfCommand,
)
from app.application.use_cases.add_history_record import AddMedicalHistoryRecordUseCaseImpl
from app.application.use_cases.export_history_pdf import ExportMedicalHistoryPdfUseCaseImpl
from app.domain import domain_events as events

pytestmark = pytest.mark.unit


def _exporter(record_repo, export_repo, pdf, storage, publisher, clock, ids):
    """Construye el caso de uso con fakes."""
    return ExportMedicalHistoryPdfUseCaseImpl(
        record_repo, export_repo, pdf, storage, publisher, clock, ids
    )


async def _seed(record_repo, publisher, clock, ids, n=2):
    """Siembra n registros del user-1."""
    adder = AddMedicalHistoryRecordUseCaseImpl(record_repo, publisher, clock, ids)
    for i in range(n):
        await adder.execute(
            AddMedicalHistoryRecordCommand(
                user_id="user-1",
                category=f"Cat-{i}",
                description=f"Desc-{i}",
                correlation_id="seed",
            )
        )
    publisher.published.clear()


async def test_happy_path(record_repo, export_repo, pdf, storage, publisher, clock, ids, now_utc):
    """Genera PDF, lo guarda, registra el export y publica MedicalHistoryPdfGenerated."""
    await _seed(record_repo, publisher, clock, ids)

    result = await _exporter(record_repo, export_repo, pdf, storage, publisher, clock, ids).execute(
        ExportMedicalHistoryPdfCommand(user_id="user-1", correlation_id="corr-5")
    )

    assert result.record_count == 2
    assert result.generated_at == now_utc
    assert storage.items[result.pdf_id].startswith(b"%PDF")
    assert await export_repo.get_by_id(result.pdf_id) is not None
    assert [type(e) for e in publisher.events] == [events.MedicalHistoryPdfGenerated]
    (generated,) = publisher.events
    assert (generated.pdf_id, generated.user_id, generated.record_count) == (
        result.pdf_id,
        "user-1",
        2,
    )


async def test_empty_history_raises(record_repo, export_repo, pdf, storage, publisher, clock, ids):
    """Sin registros -> EmptyMedicalHistory, sin storage ni eventos."""
    with pytest.raises(EmptyMedicalHistory):
        await _exporter(record_repo, export_repo, pdf, storage, publisher, clock, ids).execute(
            ExportMedicalHistoryPdfCommand(user_id="user-1", correlation_id="c")
        )
    assert storage.items == {}
    assert publisher.events == []


async def test_publish_failure_raises(record_repo, export_repo, pdf, storage, publisher, clock, ids):
    """Fallo al publicar -> EventPublishError (el export ya quedó guardado)."""
    await _seed(record_repo, publisher, clock, ids)
    publisher.fail_next = RuntimeError("bus caído")
    with pytest.raises(EventPublishError):
        await _exporter(record_repo, export_repo, pdf, storage, publisher, clock, ids).execute(
            ExportMedicalHistoryPdfCommand(user_id="user-1", correlation_id="c")
        )
