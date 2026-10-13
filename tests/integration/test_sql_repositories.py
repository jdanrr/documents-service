"""Ejemplo de test de integración SQL (PostgreSQL real del docker-compose)."""

import os

import pytest

pytestmark = pytest.mark.integration


@pytest.mark.skipif(
    os.getenv("DATABASE_URL") is None,
    reason="Requiere DATABASE_URL al PostgreSQL del compose.",
)
def test_sql_repository_placeholder():
    """Ejemplo trivial que pasa cuando hay BD (placeholder)."""
    # TODO: crear Session, migrar, guardar Authorization y verificar round-trip ORM<->dominio.
    assert True
