"""Tests de dominio: MedicalHistoryExport (validaciones)."""

import pytest

from app.domain.entities import MedicalHistoryExport
from app.domain.exceptions import InvalidFieldError

pytestmark = pytest.mark.unit


def test_export_valid(sample_user_id, now_utc):
    """Una exportación válida conserva sus datos."""
    export = MedicalHistoryExport(
        pdf_id="pdf-1", user_id=sample_user_id, record_count=3, generated_at=now_utc
    )
    assert export.record_count == 3


def test_negative_record_count_raises(sample_user_id, now_utc):
    """record_count negativo es inválido."""
    with pytest.raises(InvalidFieldError) as exc:
        MedicalHistoryExport(
            pdf_id="pdf-1", user_id=sample_user_id, record_count=-1, generated_at=now_utc
        )
    assert exc.value.field == "record_count"


def test_zero_records_allowed(sample_user_id, now_utc):
    """record_count cero es válido a nivel de dominio (el caso de uso lo rechaza)."""
    export = MedicalHistoryExport(
        pdf_id="pdf-1", user_id=sample_user_id, record_count=0, generated_at=now_utc
    )
    assert export.record_count == 0
