"""Fixtures compartidos: factories de entidades, BD con rollback y TestClient."""

import uuid
from datetime import datetime, timezone

import pytest

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
    return datetime.now(timezone.utc)
