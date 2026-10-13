"""Tests de propagación de EventPublishError (el fake falla con el propio error)."""

import pytest

from app.application.errors import EventPublishError
from app.application.ports.input.use_cases import (
    AddMedicalHistoryRecordCommand,
    ExportMedicalHistoryPdfCommand,
    GenerateAffiliationCertificateCommand,
    IssueAuthorizationCommand,
    UpdateMedicalHistoryRecordCommand,
)
from app.application.use_cases.add_history_record import AddMedicalHistoryRecordUseCaseImpl
from app.application.use_cases.export_history_pdf import ExportMedicalHistoryPdfUseCaseImpl
from app.application.use_cases.generate_certificate import (
    GenerateAffiliationCertificateUseCaseImpl,
)
from app.application.use_cases.issue_authorization import IssueAuthorizationUseCaseImpl
from app.application.use_cases.update_history_record import (
    UpdateMedicalHistoryRecordUseCaseImpl,
)

pytestmark = pytest.mark.unit


async def _seed_record(record_repo, publisher, clock, ids):
    """Siembra un registro y retorna su id."""
    adder = AddMedicalHistoryRecordUseCaseImpl(record_repo, publisher, clock, ids)
    record = await adder.execute(
        AddMedicalHistoryRecordCommand(
            user_id="user-1", category="c", description="d", correlation_id="seed"
        )
    )
    publisher.published.clear()
    return record.record_id


async def test_issue_passthrough(auth_repo, publisher, clock, ids):
    """EventPublishError del publisher se propaga tal cual."""
    publisher.fail_next = EventPublishError("caído")
    use_case = IssueAuthorizationUseCaseImpl(auth_repo, publisher, clock, ids)
    with pytest.raises(EventPublishError):
        await use_case.execute(
            IssueAuthorizationCommand(
                user_id="u", procedure="p", doctor="d", location="l", correlation_id="c"
            )
        )


async def test_certificate_passthrough(cert_repo, publisher, clock, ids):
    """EventPublishError del publisher se propaga tal cual."""
    publisher.fail_next = EventPublishError("caído")
    use_case = GenerateAffiliationCertificateUseCaseImpl(cert_repo, publisher, clock, ids)
    with pytest.raises(EventPublishError):
        await use_case.execute(
            GenerateAffiliationCertificateCommand(user_id="u", correlation_id="c")
        )


async def test_add_passthrough_and_generic_failure(record_repo, publisher, clock, ids):
    """EventPublishError se propaga; un fallo genérico se envuelve."""
    adder = AddMedicalHistoryRecordUseCaseImpl(record_repo, publisher, clock, ids)
    publisher.fail_next = EventPublishError("caído")
    with pytest.raises(EventPublishError):
        await adder.execute(
            AddMedicalHistoryRecordCommand(
                user_id="u", category="c", description="d", correlation_id="x"
            )
        )
    publisher.fail_next = RuntimeError("bus caído")
    with pytest.raises(EventPublishError):
        await adder.execute(
            AddMedicalHistoryRecordCommand(
                user_id="u", category="c", description="d", correlation_id="x"
            )
        )


async def test_update_passthrough(record_repo, publisher, clock, ids):
    """EventPublishError del publisher se propaga tal cual."""
    record_id = await _seed_record(record_repo, publisher, clock, ids)
    publisher.fail_next = EventPublishError("caído")
    use_case = UpdateMedicalHistoryRecordUseCaseImpl(record_repo, publisher, clock)
    with pytest.raises(EventPublishError):
        await use_case.execute(
            UpdateMedicalHistoryRecordCommand(
                record_id=record_id,
                user_id="user-1",
                category="c",
                description="d",
                correlation_id="x",
            )
        )


async def test_export_passthrough(record_repo, export_repo, pdf, storage, publisher, clock, ids):
    """EventPublishError del publisher se propaga tal cual."""
    await _seed_record(record_repo, publisher, clock, ids)
    publisher.fail_next = EventPublishError("caído")
    use_case = ExportMedicalHistoryPdfUseCaseImpl(
        record_repo, export_repo, pdf, storage, publisher, clock, ids
    )
    with pytest.raises(EventPublishError):
        await use_case.execute(
            ExportMedicalHistoryPdfCommand(user_id="user-1", correlation_id="x")
        )
