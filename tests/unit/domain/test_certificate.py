"""Tests de dominio: AffiliationCertificate (validaciones y transiciones)."""

from datetime import datetime

import pytest

from app.domain.entities import AffiliationCertificate
from app.domain.enums import DocumentStatus
from app.domain.exceptions import (
    InvalidFieldError,
    InvalidStatusTransitionError,
)

pytestmark = pytest.mark.unit


def test_certificate_valid(sample_user_id, now_utc):
    """Un certificado válido se crea con ISSUED."""
    cert = AffiliationCertificate(cert_id="cert-1", user_id=sample_user_id, issued_at=now_utc)
    assert cert.status == DocumentStatus.ISSUED


def test_blank_user_id_raises(now_utc):
    """user_id es obligatorio."""
    with pytest.raises(InvalidFieldError):
        AffiliationCertificate(cert_id="cert-1", user_id="", issued_at=now_utc)


def test_naive_issued_at_raises(sample_user_id):
    """issued_at sin zona horaria es inválido."""
    naive = datetime(2026, 1, 15, 12, 0, 0)
    with pytest.raises(InvalidFieldError):
        AffiliationCertificate(cert_id="cert-1", user_id=sample_user_id, issued_at=naive)


def test_mark_sent_and_failed(sample_user_id, now_utc):
    """ISSUED -> SENT y ISSUED -> FAILED son válidas."""
    cert = AffiliationCertificate(cert_id="c1", user_id=sample_user_id, issued_at=now_utc)
    cert.mark_sent()
    assert cert.status == DocumentStatus.SENT
    cert2 = AffiliationCertificate(cert_id="c2", user_id=sample_user_id, issued_at=now_utc)
    cert2.mark_failed()
    assert cert2.status == DocumentStatus.FAILED


@pytest.mark.parametrize("final", [DocumentStatus.SENT, DocumentStatus.FAILED])
def test_final_states_reject_any_transition(sample_user_id, now_utc, final):
    """SENT y FAILED son finales."""
    cert = AffiliationCertificate(
        cert_id="c", user_id=sample_user_id, issued_at=now_utc, status=final
    )
    with pytest.raises(InvalidStatusTransitionError):
        cert.mark_sent()
    with pytest.raises(InvalidStatusTransitionError):
        cert.mark_failed()
