"""Tests de AddMedicalHistoryRecord y UpdateMedicalHistoryRecord."""

import pytest

from app.application.errors import EventPublishError, Forbidden, NotFound
from app.application.ports.input.use_cases import (
    AddMedicalHistoryRecordCommand,
    UpdateMedicalHistoryRecordCommand,
)
from app.application.use_cases.add_history_record import AddMedicalHistoryRecordUseCaseImpl
from app.application.use_cases.update_history_record import (
    UpdateMedicalHistoryRecordUseCaseImpl,
)
from app.domain import domain_events as events
from app.domain.enums import DocumentOperation, DocumentType
from app.domain.exceptions import InvalidFieldError

pytestmark = pytest.mark.unit


async def _add(record_repo, publisher, clock, ids, **overrides):
    """Atajo: ejecuta el alta con valores válidos por defecto."""
    data = {
        "user_id": "user-1",
        "category": "Alergias",
        "description": "Alergia a la penicilina",
        "correlation_id": "corr-3",
    }
    data.update(overrides)
    use_case = AddMedicalHistoryRecordUseCaseImpl(record_repo, publisher, clock, ids)
    return await use_case.execute(AddMedicalHistoryRecordCommand(**data))


async def test_add_publishes_only_audit(record_repo, publisher, clock, ids, now_utc):
    """El alta publica solo DocumentsUpdated (CREATE), nada a Notifications."""
    result = await _add(record_repo, publisher, clock, ids)

    assert result.added_at == now_utc == result.updated_at
    assert [type(e) for e in publisher.events] == [events.DocumentsUpdated]
    (updated,) = publisher.events
    assert (updated.document_type, updated.operation, updated.user_id) == (
        DocumentType.MEDICAL_HISTORY_RECORD,
        DocumentOperation.CREATE,
        "user-1",
    )


async def test_add_blank_category_publishes_nothing(record_repo, publisher, clock, ids):
    """Validación fallida -> sin guardado ni eventos."""
    with pytest.raises(InvalidFieldError):
        await _add(record_repo, publisher, clock, ids, category=" ")
    assert publisher.events == []
    assert await record_repo.list_by_user_id("user-1") == []


async def test_update_happy_path(record_repo, publisher, clock, ids):
    """Actualiza campos, guarda y publica DocumentsUpdated (UPDATE)."""
    created = await _add(record_repo, publisher, clock, ids)
    publisher.published.clear()

    use_case = UpdateMedicalHistoryRecordUseCaseImpl(record_repo, publisher, clock)
    result = await use_case.execute(
        UpdateMedicalHistoryRecordCommand(
            record_id=created.record_id,
            user_id="user-1",
            category="Vacunas",
            description="Refuerzo aplicado",
            correlation_id="corr-4",
        )
    )

    assert (result.category, result.description) == ("Vacunas", "Refuerzo aplicado")
    assert [type(e) for e in publisher.events] == [events.DocumentsUpdated]
    (updated,) = publisher.events
    assert updated.operation == DocumentOperation.UPDATE
    assert updated.document_id == created.record_id


async def test_update_missing_raises_not_found(record_repo, publisher, clock):
    """Registro inexistente -> NotFound, sin eventos."""
    use_case = UpdateMedicalHistoryRecordUseCaseImpl(record_repo, publisher, clock)
    with pytest.raises(NotFound):
        await use_case.execute(
            UpdateMedicalHistoryRecordCommand(
                record_id="no-existe",
                user_id="user-1",
                category="x",
                description="y",
                correlation_id="c",
            )
        )
    assert publisher.events == []


async def test_update_other_owner_raises_forbidden(record_repo, publisher, clock, ids):
    """Dueño distinto -> Forbidden, sin cambios ni eventos."""
    created = await _add(record_repo, publisher, clock, ids)
    use_case = UpdateMedicalHistoryRecordUseCaseImpl(record_repo, publisher, clock)
    with pytest.raises(Forbidden):
        await use_case.execute(
            UpdateMedicalHistoryRecordCommand(
                record_id=created.record_id,
                user_id="otro-usuario",
                category="x",
                description="y",
                correlation_id="c",
            )
        )
    stored = await record_repo.get_by_id(created.record_id)
    assert stored.category == "Alergias"
    assert len(publisher.events) == 1  # Solo el CREATE del alta.


async def test_update_publish_failure_raises(record_repo, publisher, clock, ids):
    """Fallo al publicar -> EventPublishError."""
    created = await _add(record_repo, publisher, clock, ids)
    publisher.fail_next = RuntimeError("bus caído")
    use_case = UpdateMedicalHistoryRecordUseCaseImpl(record_repo, publisher, clock)
    with pytest.raises(EventPublishError):
        await use_case.execute(
            UpdateMedicalHistoryRecordCommand(
                record_id=created.record_id,
                user_id="user-1",
                category="Vacunas",
                description="z",
                correlation_id="c",
            )
        )
