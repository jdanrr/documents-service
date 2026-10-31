"""Tests de API: POST /certificates (401, 404, 201)."""

from datetime import datetime, timedelta, timezone

import jwt
import pytest
from fastapi.testclient import TestClient

from app.application.use_cases.generate_certificate import (
    GenerateAffiliationCertificateUseCaseImpl,
)
from app.domain.entities import ProfileSnapshot
from app.infrastructure.api.security import CurrentUser, get_current_user
from app.infrastructure.config.composition import get_generate_certificate_use_case
from app.infrastructure.config.settings import Settings
from app.main import create_app

pytestmark = pytest.mark.unit

USER_ID = "0192b3c4-7d8e-7f10-a2b3-4c5d6e7f8000"
SECRET = "dev-only-insecure-secret"


def _token(secret: str = SECRET, **claims) -> str:
    """Firma un token de prueba (HS256, con exp)."""
    payload = {
        "userId": USER_ID,
        "email": "maria.gomez@example.com",
        "firstName": "Maria Fernanda",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
    }
    payload.update(claims)
    return jwt.encode(payload, secret, algorithm="HS256")


def _seed_snapshot(snapshot_repo) -> None:
    """Siembra el titular que coincide con el token de prueba."""
    snapshot_repo.items[USER_ID] = ProfileSnapshot(
        user_id=USER_ID,
        document_type="CC",
        document_number="1020304050",
        first_name="Maria Fernanda",
        last_name="Gomez Rojas",
        affiliation_start_date=datetime(2020, 6, 15, 12, 0, 0, tzinfo=timezone.utc),
    )


def _client_with_fakes(snapshot_repo, cert_repo, pdf, storage, publisher, clock, ids):
    """App con caso de uso real cableado a fakes y usuario fijo."""
    app = create_app()
    app.dependency_overrides[get_generate_certificate_use_case] = (
        lambda: GenerateAffiliationCertificateUseCaseImpl(
            snapshot_repo, cert_repo, pdf, storage, publisher, clock, ids
        )
    )
    app.dependency_overrides[get_current_user] = lambda: CurrentUser(
        user_id=USER_ID,
        email="maria.gomez@example.com",
        first_name="Maria Fernanda",
    )
    return TestClient(app)


def test_missing_token_is_401(snapshot_repo, cert_repo, pdf, storage, publisher, clock, ids):
    """Sin Bearer token: 401."""
    app = create_app()
    client = TestClient(app)
    response = client.post("/certificates", headers={"X-Correlation-Id": "c"})
    assert response.status_code == 401


def test_invalid_token_is_401(snapshot_repo, cert_repo, pdf, storage, publisher, clock, ids):
    """Token con firma inválida: 401 (sin overrides de seguridad)."""
    app = create_app()
    client = TestClient(app)
    response = client.post(
        "/certificates",
        headers={"Authorization": f"Bearer {_token(secret='otra-clave')}"},
    )
    assert response.status_code == 401


def test_missing_snapshot_is_404(snapshot_repo, cert_repo, pdf, storage, publisher, clock, ids):
    """Sin titular: 404 con mensaje claro."""
    client = _client_with_fakes(
        snapshot_repo, cert_repo, pdf, storage, publisher, clock, ids
    )
    response = client.post("/certificates")
    assert response.status_code == 404
    assert "perfil" in response.json()["detail"].lower()


def test_happy_path_returns_201_with_aliases(
    snapshot_repo, cert_repo, pdf, storage, publisher, clock, ids, now_utc
):
    """Con titular: 201 y cuerpo {certificateId, issuedAt, affiliationStartDate}."""
    _seed_snapshot(snapshot_repo)
    client = _client_with_fakes(
        snapshot_repo, cert_repo, pdf, storage, publisher, clock, ids
    )
    response = client.post(
        "/certificates", headers={"X-Correlation-Id": "corr-api-1"}
    )
    assert response.status_code == 201
    body = response.json()
    assert set(body) == {"certificateId", "issuedAt", "affiliationStartDate"}
    assert body["affiliationStartDate"].startswith("2020-06-15")
    [(batch, correlation_id)] = publisher.published
    assert correlation_id == "corr-api-1"
    assert len(batch) == 1


def test_real_security_dependency_accepts_valid_token(
    snapshot_repo, cert_repo, pdf, storage, publisher, clock, ids
):
    """Sin override de seguridad: el JWT válido pasa y el resto del flujo es 201."""
    _seed_snapshot(snapshot_repo)
    app = create_app()
    app.dependency_overrides[get_generate_certificate_use_case] = (
        lambda: GenerateAffiliationCertificateUseCaseImpl(
            snapshot_repo, cert_repo, pdf, storage, publisher, clock, ids
        )
    )
    client = TestClient(app)
    response = client.post(
        "/certificates", headers={"Authorization": f"Bearer {_token()}"}
    )
    assert response.status_code == 201
    assert Settings().jwt_secret == SECRET
