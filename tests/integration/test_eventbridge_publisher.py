"""Ejemplo de test del publisher EventBridge con moto (sobre estándar)."""

import pytest

pytestmark = pytest.mark.integration


def test_eventbridge_envelope_shape_placeholder():
    """Ejemplo trivial que pasa: verifica la forma del sobre esperado."""
    # TODO: con moto (@mock_aws events): crear bus, publicar AuthorizationIssued
    # TODO: y verificar source/detail-type/detail.metadata/detail.data.
    envelope = {
        "source": "kenko.documents",
        "detail-type": "AuthorizationIssued",
        "detail": {"metadata": {}, "data": {}},
    }
    assert envelope["source"] == "kenko.documents"
