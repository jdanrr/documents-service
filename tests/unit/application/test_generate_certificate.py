"""Tests de GenerateAffiliationCertificate (feliz, errores y eventos)."""

from datetime import datetime, timezone

import pytest

from app.application.errors import EventPublishError, ProfileNotFound, StorageError
from app.application.ports.input.use_cases import GenerateAffiliationCertificateCommand
from app.application.use_cases.generate_certificate import (
    GenerateAffiliationCertificateUseCaseImpl,
)
from app.domain import domain_events as events
from app.domain.entities import ProfileSnapshot
from app.domain.enums import DocumentStatus

pytestmark = pytest.mark.unit

AFFILIATION_START = datetime(2020, 6, 15, 12, 0, 0, tzinfo=timezone.utc)


def _seed_snapshot(snapshot_repo, user_id: str = "user-1") -> ProfileSnapshot:
    """Siembra el titular de prueba y lo retorna."""
    snapshot = ProfileSnapshot(
        user_id=user_id,
        document_type="CC",
        document_number="1020304050",
        first_name="Maria Fernanda",
        last_name="Gomez Rojas",
        affiliation_start_date=AFFILIATION_START,
    )
    snapshot_repo.items[user_id] = snapshot
    return snapshot


def _use_case(snapshot_repo, cert_repo, pdf, storage, publisher, clock, ids):
    """Construye el caso de uso con fakes."""
    return GenerateAffiliationCertificateUseCaseImpl(
        snapshot_repo, cert_repo, pdf, storage, publisher, clock, ids
    )


def _command(user_id: str = "user-1", correlation_id: str = "corr-1"):
    """Comando válido (email y nombre salen del JWT)."""
    return GenerateAffiliationCertificateCommand(
        user_id=user_id,
        email="maria.gomez@example.com",
        first_name="Maria Fernanda",
        correlation_id=correlation_id,
    )


async def test_happy_path(
    snapshot_repo, cert_repo, pdf, storage, publisher, clock, ids, now_utc
):
    """PDF -> S3 -> BD -> bus; la fecha de afiliación se copia del titular."""
    _seed_snapshot(snapshot_repo)
    use_case = _use_case(snapshot_repo, cert_repo, pdf, storage, publisher, clock, ids)

    result = await use_case.execute(_command(correlation_id="corr-2"))

    assert result.status == DocumentStatus.ISSUED
    assert result.issued_at == now_utc
    assert result.affiliation_start_date == AFFILIATION_START
    assert result.file_key == f"certificates/user-1/{result.cert_id}.pdf"
    assert storage.items[result.file_key].startswith(b"%PDF")
    assert await cert_repo.get_by_id(result.cert_id) is not None
    assert [type(e) for e in publisher.events] == [events.CertificateGenerated]
    (generated,) = publisher.events
    assert (generated.cert_id, generated.user_id) == (result.cert_id, "user-1")
    assert (generated.email, generated.first_name) == (
        "maria.gomez@example.com",
        "Maria Fernanda",
    )
    assert generated.issued_at == now_utc
    assert generated.file_key == result.file_key
    assert generated.file_name == f"certificado-afiliacion-{result.cert_id}.pdf"
    [(batch, correlation_id)] = publisher.published
    assert correlation_id == "corr-2"
    assert batch == [generated]


async def test_missing_snapshot_raises_404_nothing_happens(
    snapshot_repo, cert_repo, pdf, storage, publisher, clock, ids
):
    """Sin titular: ProfileNotFound, sin PDF, sin S3, sin eventos."""
    use_case = _use_case(snapshot_repo, cert_repo, pdf, storage, publisher, clock, ids)
    with pytest.raises(ProfileNotFound):
        await use_case.execute(_command())
    assert storage.items == {}
    assert publisher.events == []
    assert await cert_repo.list_by_user_id("user-1") == []


async def test_storage_failure_saves_nothing(
    snapshot_repo, cert_repo, pdf, storage, publisher, clock, ids
):
    """Fallo al subir: StorageError, sin guardar ni publicar."""
    _seed_snapshot(snapshot_repo)
    storage.fail_with_storage_error()
    use_case = _use_case(snapshot_repo, cert_repo, pdf, storage, publisher, clock, ids)
    with pytest.raises(StorageError):
        await use_case.execute(_command())
    assert await cert_repo.list_by_user_id("user-1") == []
    assert publisher.events == []


async def test_generic_storage_failure_wraps_to_storage_error(
    snapshot_repo, cert_repo, pdf, storage, publisher, clock, ids
):
    """Un fallo genérico del storage se envuelve en StorageError."""
    _seed_snapshot(snapshot_repo)
    storage.fail_next = RuntimeError("disco lleno")
    use_case = _use_case(snapshot_repo, cert_repo, pdf, storage, publisher, clock, ids)
    with pytest.raises(StorageError):
        await use_case.execute(_command())
    assert await cert_repo.list_by_user_id("user-1") == []
    assert publisher.events == []


async def test_publish_failure_keeps_saved_certificate(
    snapshot_repo, cert_repo, pdf, storage, publisher, clock, ids
):
    """Fallo al publicar: EventPublishError, el certificado queda guardado."""
    _seed_snapshot(snapshot_repo)
    publisher.fail_next = RuntimeError("bus caído")
    use_case = _use_case(snapshot_repo, cert_repo, pdf, storage, publisher, clock, ids)
    with pytest.raises(EventPublishError):
        await use_case.execute(_command())
    saved = await cert_repo.list_by_user_id("user-1")
    assert len(saved) == 1
    assert storage.items[saved[0].file_key].startswith(b"%PDF")
