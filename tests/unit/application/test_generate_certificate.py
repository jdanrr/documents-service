"""Tests de GenerateAffiliationCertificate (feliz, errores y eventos)."""

import pytest

from app.application.errors import EventPublishError
from app.application.ports.input.use_cases import GenerateAffiliationCertificateCommand
from app.application.use_cases.generate_certificate import (
    GenerateAffiliationCertificateUseCaseImpl,
)
from app.domain import domain_events as events
from app.domain.enums import DocumentOperation, DocumentStatus, DocumentType
from app.domain.exceptions import InvalidFieldError

pytestmark = pytest.mark.unit


async def test_happy_path(cert_repo, publisher, clock, ids, now_utc):
    """Crea con ISSUED, guarda y publica CertificateGenerated + DocumentsUpdated."""
    use_case = GenerateAffiliationCertificateUseCaseImpl(cert_repo, publisher, clock, ids)
    result = await use_case.execute(
        GenerateAffiliationCertificateCommand(user_id="user-1", correlation_id="corr-2")
    )

    assert result.status == DocumentStatus.ISSUED
    assert result.issued_at == now_utc
    assert [type(e) for e in publisher.events] == [
        events.CertificateGenerated,
        events.DocumentsUpdated,
    ]
    generated, updated = publisher.events
    assert (generated.cert_id, generated.user_id) == (result.cert_id, "user-1")
    assert (updated.document_type, updated.operation) == (
        DocumentType.AFFILIATION_CERTIFICATE,
        DocumentOperation.CREATE,
    )


async def test_blank_user_publishes_nothing(cert_repo, publisher, clock, ids):
    """Sin user_id no se guarda ni se publica."""
    use_case = GenerateAffiliationCertificateUseCaseImpl(cert_repo, publisher, clock, ids)
    with pytest.raises(InvalidFieldError):
        await use_case.execute(
            GenerateAffiliationCertificateCommand(user_id="", correlation_id="c")
        )
    assert publisher.events == []


async def test_publish_failure_raises(cert_repo, publisher, clock, ids):
    """Fallo al publicar -> EventPublishError."""
    publisher.fail_next = RuntimeError("bus caído")
    use_case = GenerateAffiliationCertificateUseCaseImpl(cert_repo, publisher, clock, ids)
    with pytest.raises(EventPublishError):
        await use_case.execute(
            GenerateAffiliationCertificateCommand(user_id="user-1", correlation_id="c")
        )
