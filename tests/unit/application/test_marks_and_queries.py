"""Tests de marks (SENT/FAILED) y consultas (sin eventos)."""

import pytest

from app.application.errors import NotFound
from app.application.ports.input.use_cases import (
    AddMedicalHistoryRecordCommand,
    GenerateAffiliationCertificateCommand,
    GetAffiliationCertificateCommand,
    GetAuthorizationCommand,
    IssueAuthorizationCommand,
    ListMedicalHistoryRecordsCommand,
    MarkAuthorizationCommand,
    MarkCertificateCommand,
)
from app.application.use_cases.add_history_record import AddMedicalHistoryRecordUseCaseImpl
from app.application.use_cases.generate_certificate import (
    GenerateAffiliationCertificateUseCaseImpl,
)
from app.application.use_cases.issue_authorization import IssueAuthorizationUseCaseImpl
from app.application.use_cases.mark_authorization import (
    MarkAuthorizationDeliveredUseCaseImpl,
    MarkAuthorizationDeliveryFailedUseCaseImpl,
)
from app.application.use_cases.mark_certificate import (
    MarkCertificateDeliveredUseCaseImpl,
    MarkCertificateDeliveryFailedUseCaseImpl,
)
from app.application.use_cases.queries import (
    GetAffiliationCertificateUseCaseImpl,
    GetAuthorizationUseCaseImpl,
    ListMedicalHistoryRecordsUseCaseImpl,
)
from app.domain.enums import DocumentStatus
from app.domain.exceptions import InvalidStatusTransitionError

pytestmark = pytest.mark.unit


async def _issue(auth_repo, publisher, clock, ids):
    """Emite una autorización de ejemplo."""
    use_case = IssueAuthorizationUseCaseImpl(auth_repo, publisher, clock, ids)
    return await use_case.execute(
        IssueAuthorizationCommand(
            user_id="user-1",
            procedure="p",
            doctor="d",
            location="l",
            correlation_id="c",
        )
    )


async def _cert(cert_repo, publisher, clock, ids):
    """Genera un certificado de ejemplo."""
    use_case = GenerateAffiliationCertificateUseCaseImpl(cert_repo, publisher, clock, ids)
    return await use_case.execute(
        GenerateAffiliationCertificateCommand(user_id="user-1", correlation_id="c")
    )


async def test_mark_authorization_delivered(auth_repo, publisher, clock, ids):
    """ISSUED -> SENT guarda y no publica nada nuevo."""
    created = await _issue(auth_repo, publisher, clock, ids)
    before = len(publisher.events)
    result = await MarkAuthorizationDeliveredUseCaseImpl(auth_repo).execute(
        MarkAuthorizationCommand(auth_id=created.auth_id)
    )
    assert result.status == DocumentStatus.SENT
    assert len(publisher.events) == before


async def test_mark_authorization_failed(auth_repo, publisher, clock, ids):
    """ISSUED -> FAILED guarda y no publica nada nuevo."""
    created = await _issue(auth_repo, publisher, clock, ids)
    result = await MarkAuthorizationDeliveryFailedUseCaseImpl(auth_repo).execute(
        MarkAuthorizationCommand(auth_id=created.auth_id)
    )
    assert result.status == DocumentStatus.FAILED


async def test_mark_missing_authorization_raises(auth_repo):
    """Marcar inexistente -> NotFound (ambas variantes)."""
    with pytest.raises(NotFound):
        await MarkAuthorizationDeliveredUseCaseImpl(auth_repo).execute(
            MarkAuthorizationCommand(auth_id="no-existe")
        )
    with pytest.raises(NotFound):
        await MarkAuthorizationDeliveryFailedUseCaseImpl(auth_repo).execute(
            MarkAuthorizationCommand(auth_id="no-existe")
        )


async def test_mark_sent_twice_raises(auth_repo, publisher, clock, ids):
    """SENT es final: segundo cambio -> InvalidStatusTransitionError."""
    created = await _issue(auth_repo, publisher, clock, ids)
    marker = MarkAuthorizationDeliveredUseCaseImpl(auth_repo)
    await marker.execute(MarkAuthorizationCommand(auth_id=created.auth_id))
    with pytest.raises(InvalidStatusTransitionError):
        await marker.execute(MarkAuthorizationCommand(auth_id=created.auth_id))


async def test_mark_certificate_roundtrip(cert_repo, publisher, clock, ids):
    """Certificado: SENT y FAILED, más NotFound y transición inválida."""
    created = await _cert(cert_repo, publisher, clock, ids)
    sent = await MarkCertificateDeliveredUseCaseImpl(cert_repo).execute(
        MarkCertificateCommand(cert_id=created.cert_id)
    )
    assert sent.status == DocumentStatus.SENT
    with pytest.raises(InvalidStatusTransitionError):
        await MarkCertificateDeliveryFailedUseCaseImpl(cert_repo).execute(
            MarkCertificateCommand(cert_id=created.cert_id)
        )
    with pytest.raises(NotFound):
        await MarkCertificateDeliveredUseCaseImpl(cert_repo).execute(
            MarkCertificateCommand(cert_id="no-existe")
        )
    with pytest.raises(NotFound):
        await MarkCertificateDeliveryFailedUseCaseImpl(cert_repo).execute(
            MarkCertificateCommand(cert_id="no-existe")
        )
    fresh = await _cert(cert_repo, publisher, clock, ids)
    failed = await MarkCertificateDeliveryFailedUseCaseImpl(cert_repo).execute(
        MarkCertificateCommand(cert_id=fresh.cert_id)
    )
    assert failed.status == DocumentStatus.FAILED


async def test_queries(auth_repo, cert_repo, record_repo, publisher, clock, ids):
    """Get/List: camino feliz y NotFound."""
    created = await _issue(auth_repo, publisher, clock, ids)
    found = await GetAuthorizationUseCaseImpl(auth_repo).execute(
        GetAuthorizationCommand(auth_id=created.auth_id)
    )
    assert found.auth_id == created.auth_id
    with pytest.raises(NotFound):
        await GetAuthorizationUseCaseImpl(auth_repo).execute(
            GetAuthorizationCommand(auth_id="no-existe")
        )

    cert = await _cert(cert_repo, publisher, clock, ids)
    found_cert = await GetAffiliationCertificateUseCaseImpl(cert_repo).execute(
        GetAffiliationCertificateCommand(cert_id=cert.cert_id)
    )
    assert found_cert.cert_id == cert.cert_id
    with pytest.raises(NotFound):
        await GetAffiliationCertificateUseCaseImpl(cert_repo).execute(
            GetAffiliationCertificateCommand(cert_id="no-existe")
        )

    adder = AddMedicalHistoryRecordUseCaseImpl(record_repo, publisher, clock, ids)
    await adder.execute(
        AddMedicalHistoryRecordCommand(
            user_id="user-1", category="c", description="d", correlation_id="x"
        )
    )
    records = await ListMedicalHistoryRecordsUseCaseImpl(record_repo).execute(
        ListMedicalHistoryRecordsCommand(user_id="user-1")
    )
    assert len(records) == 1
    assert await ListMedicalHistoryRecordsUseCaseImpl(record_repo).execute(
        ListMedicalHistoryRecordsCommand(user_id="otro")
    ) == []
