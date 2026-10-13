"""Ejemplo de test de API (TestClient contra GET /health)."""

from fastapi.testclient import TestClient

from app.main import create_app


def test_health_endpoint():
    """El endpoint de salud responde 200."""
    # TODO: usar dependency_overrides para inyectar fakes en endpoints reales.
    client = TestClient(create_app())
    response = client.get("/health")
    assert response.status_code == 200
