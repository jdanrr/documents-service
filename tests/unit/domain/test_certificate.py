"""Tests de dominio: AffiliationCertificate (validaciones y transiciones)."""

from datetime import datetime, timezone

import pytest

from app.domain.entities import AffiliationCertificate
from app.domain.enums import DocumentStatus
from app.domain.exceptions import (
    InvalidFieldError,
    InvalidStatusTransitionError,
)

pytestmark = pytest.mark.unit


def _affiliation_start() -> datetime:
    """Fecha de afiliación de ejemplo (UTC)."""
    return datetime(2020, 6, 15, 12, 0, 0, tzinfo=timezone.utc)


def test_certificate_valid(sample_user_id, now_utc):
    """Un certificado válido se crea con ISSUED y foto fija de la afiliación."""
    cert = AffiliationCertificate(
        cert_id="cert-1",
        user_id=sample_user_id,
        affiliation_start_date=_affiliation_start(),
        issued_at=now_utc,
    )
    assert cert.status == DocumentStatus.ISSUED
    assert cert.affiliation_start_date == _affiliation_start()
    assert cert.file_key == ""


def test_blank_user_id_raises(now_utc):
    """user_id es obligatorio."""
    with pytest.raises(InvalidFieldError):
        AffiliationCertificate(
            cert_id="cert-1",
            user_id="",
            affiliation_start_date=_affiliation_start(),
            issued_at=now_utc,
        )


def test_naive_affiliation_start_date_raises(sample_user_id, now_utc):
    """affiliation_start_date sin zona horaria es inválida."""
    naive = datetime(2020, 6, 15, 12, 0, 0)
    with pytest.raises(InvalidFieldError):
        AffiliationCertificate(
            cert_id="cert-1",
            user_id=sample_user_id,
            affiliation_start_date=naive,
            issued_at=now_utc,
        )


def test_naive_issued_at_raises(sample_user_id):
    """issued_at sin zona horaria es inválido."""
    naive = datetime(2026, 1, 15, 12, 0, 0)
    with pytest.raises(InvalidFieldError):
        AffiliationCertificate(
            cert_id="cert-1",
            user_id=sample_user_id,
            affiliation_start_date=_affiliation_start(),
            issued_at=naive,
        )


def test_mark_sent_and_failed(sample_user_id, now_utc):
    """ISSUED -> SENT y ISSUED -> FAILED son válidas."""
    cert = AffiliationCertificate(
        cert_id="c1",
        user_id=sample_user_id,
        affiliation_start_date=_affiliation_start(),
        issued_at=now_utc,
    )
    cert.mark_sent()
    assert cert.status == DocumentStatus.SENT
    cert2 = AffiliationCertificate(
        cert_id="c2",
        user_id=sample_user_id,
        affiliation_start_date=_affiliation_start(),
        issued_at=now_utc,
    )
    cert2.mark_failed()
    assert cert2.status == DocumentStatus.FAILED


@pytest.mark.parametrize("final", [DocumentStatus.SENT, DocumentStatus.FAILED])
def test_final_states_reject_any_transition(sample_user_id, now_utc, final):
    """SENT y FAILED son finales."""
    cert = AffiliationCertificate(
        cert_id="c",
        user_id=sample_user_id,
        affiliation_start_date=_affiliation_start(),
        issued_at=now_utc,
        status=final,
    )
    with pytest.raises(InvalidStatusTransitionError):
        cert.mark_sent()
    with pytest.raises(InvalidStatusTransitionError):
        cert.mark_failed()
