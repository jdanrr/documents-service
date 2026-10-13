"""Fixtures compartidos: factories, fakes de sistema y repositorios."""

import uuid
from datetime import datetime, timezone

import pytest

from tests.fakes.event_publisher import FakeEventPublisher
from tests.fakes.pdf_generator import FakePdfGenerator
from tests.fakes.repositories import (
    InMemoryAuthorizationRepository,
    InMemoryCertificateRepository,
    InMemoryMedicalHistoryExportRepository,
    InMemoryMedicalHistoryRecordRepository,
)
from tests.fakes.system import FakeDocumentStorage, FixedClock, SequentialIdGenerator

# TODO: fixture db_session (PostgreSQL del compose con rollback por test).
# TODO: fixture client (TestClient con dependency_overrides a fakes).
# TODO: factories make_authorization(), make_certificate(), make_record().


@pytest.fixture
def sample_user_id() -> str:
    """userId de ejemplo para los tests."""
    return f"user-{uuid.uuid4().hex[:8]}"


@pytest.fixture
def now_utc() -> datetime:
    """Fecha UTC de ejemplo."""
    return datetime(2026, 1, 15, 12, 0, 0, tzinfo=timezone.utc)


@pytest.fixture
def clock(now_utc: datetime) -> FixedClock:
    """Reloj fijo determinista."""
    return FixedClock(now_utc)


@pytest.fixture
def ids() -> SequentialIdGenerator:
    """Generador secuencial de ids."""
    return SequentialIdGenerator()


@pytest.fixture
def publisher() -> FakeEventPublisher:
    """Publisher falso que registra eventos."""
    return FakeEventPublisher()


@pytest.fixture
def auth_repo() -> InMemoryAuthorizationRepository:
    """Repo falso de autorizaciones."""
    return InMemoryAuthorizationRepository()


@pytest.fixture
def cert_repo() -> InMemoryCertificateRepository:
    """Repo falso de certificados."""
    return InMemoryCertificateRepository()


@pytest.fixture
def record_repo() -> InMemoryMedicalHistoryRecordRepository:
    """Repo falso de registros."""
    return InMemoryMedicalHistoryRecordRepository()


@pytest.fixture
def export_repo() -> InMemoryMedicalHistoryExportRepository:
    """Repo falso de exportaciones."""
    return InMemoryMedicalHistoryExportRepository()


@pytest.fixture
def pdf() -> FakePdfGenerator:
    """Generador de PDF falso."""
    return FakePdfGenerator()


@pytest.fixture
def storage() -> FakeDocumentStorage:
    """Storage falso en memoria."""
    return FakeDocumentStorage()
