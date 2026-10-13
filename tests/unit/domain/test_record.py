"""Tests de dominio: MedicalHistoryRecord (validaciones y update)."""

from datetime import timedelta

import pytest

from app.domain.entities import MedicalHistoryRecord
from app.domain.exceptions import InvalidDateOrderError, InvalidFieldError

pytestmark = pytest.mark.unit


def _make(sample_user_id, now_utc, **overrides):
    """Factory mínima de registros válidos."""
    data = {
        "record_id": "rec-1",
        "user_id": sample_user_id,
        "category": "Alergias",
        "description": "Alergia a la penicilina",
        "added_at": now_utc,
        "updated_at": now_utc,
    }
    data.update(overrides)
    return MedicalHistoryRecord(**data)


@pytest.mark.parametrize("field", ["category", "description"])
def test_blank_fields_raise(sample_user_id, now_utc, field):
    """category/description no aceptan vacíos ni solo espacios."""
    with pytest.raises(InvalidFieldError):
        _make(sample_user_id, now_utc, **{field: "  "})


def test_updated_before_added_raises(sample_user_id, now_utc):
    """updated_at anterior a added_at es inválido."""
    with pytest.raises(InvalidDateOrderError):
        _make(sample_user_id, now_utc, updated_at=now_utc - timedelta(hours=1))


def test_update_changes_fields(sample_user_id, now_utc):
    """update() cambia category/description/updated_at."""
    record = _make(sample_user_id, now_utc)
    later = now_utc + timedelta(days=1)
    record.update("Vacunas", "Refuerzo aplicado", later)
    assert (record.category, record.description, record.updated_at) == (
        "Vacunas",
        "Refuerzo aplicado",
        later,
    )


def test_update_with_older_date_raises(sample_user_id, now_utc):
    """update() con fecha anterior a added_at es inválido."""
    record = _make(sample_user_id, now_utc)
    with pytest.raises(InvalidDateOrderError):
        record.update("Vacunas", "Refuerzo", now_utc - timedelta(days=1))


def test_update_with_blank_raises(sample_user_id, now_utc):
    """update() valida los nuevos valores."""
    record = _make(sample_user_id, now_utc)
    with pytest.raises(InvalidFieldError):
        record.update("", "x", now_utc)
    with pytest.raises(InvalidFieldError):
        record.update("Vacunas", "   ", now_utc)
