"""Tests de dominio: Authorization (validaciones y transiciones)."""

from datetime import datetime, timedelta, timezone

import pytest

from app.domain.entities import Authorization
from app.domain.enums import DocumentStatus
from app.domain.exceptions import (
    InvalidFieldError,
    InvalidStatusTransitionError,
)

pytestmark = pytest.mark.unit


def _make(sample_user_id, now_utc, **overrides):
    """Factory mínima de autorizaciones válidas."""
    data = {
        "auth_id": "auth-1",
        "user_id": sample_user_id,
        "procedure": "Consulta general",
        "doctor": "Dra. Ejemplo",
        "location": "Sede Norte",
        "issued_at": now_utc,
    }
    data.update(overrides)
    return Authorization(**data)


def test_authorization_defaults_to_issued(sample_user_id, now_utc):
    """El estado por defecto es ISSUED."""
    assert _make(sample_user_id, now_utc).status == DocumentStatus.ISSUED


@pytest.mark.parametrize("field", ["procedure", "doctor", "location"])
@pytest.mark.parametrize("bad", ["", "   "])
def test_blank_fields_raise(sample_user_id, now_utc, field, bad):
    """procedure/doctor/location no aceptan vacíos ni solo espacios."""
    with pytest.raises(InvalidFieldError) as exc:
        _make(sample_user_id, now_utc, **{field: bad})
    assert exc.value.field == field


def test_blank_user_id_raises(now_utc):
    """user_id es obligatorio."""
    with pytest.raises(InvalidFieldError) as exc:
        _make("   ", now_utc)
    assert exc.value.field == "user_id"


def test_naive_issued_at_raises(sample_user_id):
    """issued_at sin zona horaria es inválido."""
    with pytest.raises(InvalidFieldError):
        _make(sample_user_id, datetime(2026, 1, 15, 12, 0, 0))


def test_non_utc_issued_at_raises(sample_user_id):
    """issued_at fuera de UTC es inválido."""
    bogota = timezone(timedelta(hours=-5))
    with pytest.raises(InvalidFieldError):
        _make(sample_user_id, datetime(2026, 1, 15, 12, tzinfo=bogota))


def test_mark_sent(sample_user_id, now_utc):
    """ISSUED -> SENT es válida."""
    auth = _make(sample_user_id, now_utc)
    auth.mark_sent()
    assert auth.status == DocumentStatus.SENT


def test_mark_failed(sample_user_id, now_utc):
    """ISSUED -> FAILED es válida."""
    auth = _make(sample_user_id, now_utc)
    auth.mark_failed()
    assert auth.status == DocumentStatus.FAILED


@pytest.mark.parametrize("final", [DocumentStatus.SENT, DocumentStatus.FAILED])
def test_final_states_reject_any_transition(sample_user_id, now_utc, final):
    """SENT y FAILED son finales: ningún cambio posterior es válido."""
    auth = _make(sample_user_id, now_utc, status=final)
    with pytest.raises(InvalidStatusTransitionError):
        auth.mark_sent()
    with pytest.raises(InvalidStatusTransitionError):
        auth.mark_failed()
