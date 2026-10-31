"""Tests del sobre EventBridge de CertificateGenerated (forma exacta)."""

import json
from datetime import datetime, timezone

import pytest

from app.domain import domain_events as events
from app.infrastructure.config.settings import Settings
from app.infrastructure.messaging.publishers.eventbridge_publisher import (
    EventBridgePublisher,
)

pytestmark = pytest.mark.unit


def _publisher() -> EventBridgePublisher:
    """Publisher real sin llamar a AWS (solo arma el entry)."""
    return EventBridgePublisher(
        Settings(
            documents_bucket_name="kenko-dev-documents-files",
            event_bus_name="kenko-dev-bus",
        )
    )


def _event() -> events.CertificateGenerated:
    """Evento de dominio de ejemplo."""
    return events.CertificateGenerated(
        cert_id="cert-1",
        user_id="user-1",
        email="maria.gomez@example.com",
        first_name="Maria Fernanda",
        issued_at=datetime(2026, 10, 31, 15, 0, 0, tzinfo=timezone.utc),
        file_key="certificates/user-1/cert-1.pdf",
        file_name="certificado-afiliacion-cert-1.pdf",
    )


def test_entry_shape_matches_put_events_contract():
    """Source/DetailType/EventBusName y detail con metadata + data."""
    entry = _publisher()._to_entry(_event(), "corr-1")

    assert entry["Source"] == "kenko.documents"
    assert entry["DetailType"] == "CertificateGenerated"
    assert entry["EventBusName"] == "kenko-dev-bus"
    detail = json.loads(entry["Detail"])
    assert detail["metadata"]["eventVersion"] == "1"
    assert detail["metadata"]["occurredAt"].endswith("Z")
    assert detail["metadata"]["correlationId"] == "corr-1"
    assert len(detail["metadata"]["eventId"]) == 36
    assert detail["data"]["issuedAt"] == "2026-10-31T15:00:00Z"
    assert detail["data"] == {
        "certificateId": "cert-1",
        "userId": "user-1",
        "email": "maria.gomez@example.com",
        "firstName": "Maria Fernanda",
        "issuedAt": "2026-10-31T15:00:00Z",
        "file": {
            "bucket": "kenko-dev-documents-files",
            "key": "certificates/user-1/cert-1.pdf",
            "contentType": "application/pdf",
            "fileName": "certificado-afiliacion-cert-1.pdf",
        },
    }


def test_event_ids_are_unique():
    """Cada evento lleva un eventId único."""
    first = _publisher()._to_entry(_event(), "c")
    second = _publisher()._to_entry(_event(), "c")
    assert json.loads(first["Detail"])["metadata"]["eventId"] != json.loads(
        second["Detail"]
    )["metadata"]["eventId"]
