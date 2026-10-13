"""Tests de IssueAuthorization (camino feliz, errores y eventos exactos)."""

import pytest

from app.application.errors import EventPublishError
from app.application.ports.input.use_cases import IssueAuthorizationCommand
from app.application.use_cases.issue_authorization import IssueAuthorizationUseCaseImpl
from app.domain import domain_events as events
from app.domain.enums import DocumentOperation, DocumentStatus, DocumentType
from app.domain.exceptions import InvalidFieldError

pytestmark = pytest.mark.unit


def _use_case(auth_repo, publisher, clock, ids):
    """Construye el caso de uso con fakes."""
    return IssueAuthorizationUseCaseImpl(auth_repo, publisher, clock, ids)


def _command(**overrides):
    """Comando válido por defecto."""
    data = {
        "user_id": "user-1",
        "procedure": "Resonancia",
        "doctor": "Dr. Ejemplo",
        "location": "Sede Sur",
        "correlation_id": "corr-1",
    }
    data.update(overrides)
    return IssueAuthorizationCommand(**data)


async def test_happy_path_publishes_two_events_in_order(auth_repo, publisher, clock, ids, now_utc):
    """Crea con ISSUED, guarda y publica AuthorizationIssued + DocumentsUpdated."""
    result = await _use_case(auth_repo, publisher, clock, ids).execute(_command())

    assert result.status == DocumentStatus.ISSUED
    assert result.issued_at == now_utc
    assert await auth_repo.get_by_id(result.auth_id) is not None
    assert [type(e) for e in publisher.events] == [
        events.AuthorizationIssued,
        events.DocumentsUpdated,
    ]
    issued, updated = publisher.events
    assert (issued.auth_id, issued.user_id, issued.procedure) == (
        result.auth_id,
        "user-1",
        "Resonancia",
    )
    assert (updated.document_id, updated.document_type, updated.operation) == (
        result.auth_id,
        DocumentType.AUTHORIZATION,
        DocumentOperation.CREATE,
    )
    assert publisher.published[0][1] == "corr-1"


async def test_blank_procedure_publishes_nothing(auth_repo, publisher, clock, ids):
    """Si falla la validación, no se guarda ni se publica nada."""
    with pytest.raises(InvalidFieldError):
        await _use_case(auth_repo, publisher, clock, ids).execute(_command(procedure="  "))
    assert publisher.events == []
    assert await auth_repo.list_by_user_id("user-1") == []


async def test_publish_failure_raises_event_publish_error(auth_repo, publisher, clock, ids):
    """Si publicar falla, se propaga EventPublishError (lo guardado NO se revierte)."""
    publisher.fail_next = RuntimeError("bus caído")
    with pytest.raises(EventPublishError):
        await _use_case(auth_repo, publisher, clock, ids).execute(_command())
    assert await auth_repo.list_by_user_id("user-1") != []
