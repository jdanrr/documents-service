"""Tests de dominio: ProfileSnapshot (copia mínima del titular)."""

from datetime import datetime, timezone

import pytest

from app.domain.entities import ProfileSnapshot
from app.domain.exceptions import InvalidFieldError

pytestmark = pytest.mark.unit

AFFILIATION_START = datetime(2020, 6, 15, 12, 0, 0, tzinfo=timezone.utc)


def _snapshot(user_id: str = "user-1", **overrides) -> ProfileSnapshot:
    """Construye un snapshot válido con campos sustituibles."""
    fields = {
        "user_id": user_id,
        "document_type": "CC",
        "document_number": "1020304050",
        "first_name": "Maria Fernanda",
        "last_name": "Gomez Rojas",
        "affiliation_start_date": AFFILIATION_START,
    }
    fields.update(overrides)
    return ProfileSnapshot(**fields)


def test_snapshot_valid():
    """Un snapshot válido expone el nombre completo."""
    snapshot = _snapshot()
    assert snapshot.full_name == "Maria Fernanda Gomez Rojas"


def test_blank_fields_raise():
    """Nombre y documento no pueden estar vacíos."""
    for field in ("document_type", "document_number", "first_name", "last_name"):
        with pytest.raises(InvalidFieldError):
            _snapshot(**{field: "   "})


def test_blank_user_id_raises():
    """user_id es obligatorio."""
    with pytest.raises(InvalidFieldError):
        _snapshot(user_id="")


def test_naive_affiliation_start_date_raises():
    """affiliation_start_date debe estar en UTC."""
    with pytest.raises(InvalidFieldError):
        _snapshot(affiliation_start_date=datetime(2020, 6, 15, 12, 0, 0))
