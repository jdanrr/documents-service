"""Ejemplo de test de dominio (entidades y enums, sin dependencias externas)."""

import pytest

from app.domain.entities import Authorization
from app.domain.enums import DocumentStatus

pytestmark = pytest.mark.unit


def test_authorization_defaults_to_issued(sample_user_id, now_utc):
    """Ejemplo trivial que pasa: el estado por defecto es ISSUED."""
    # TODO: ampliar batería (mark_sent/mark_failed, validaciones de dominio).
    auth = Authorization(
        auth_id="auth-1",
        user_id=sample_user_id,
        procedure="Consulta general",
        doctor="Dra. Ejemplo",
        location="Sede Norte",
        issued_at=now_utc,
    )
    assert auth.status == DocumentStatus.ISSUED
