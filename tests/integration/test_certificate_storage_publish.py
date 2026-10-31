"""Integración S3 + EventBridge con moto (sin AWS real)."""

import os

import boto3
import pytest
from moto import mock_aws

from app.application.errors import EventPublishError
from app.domain import domain_events as events
from app.domain.entities import AffiliationCertificate, ProfileSnapshot
from app.infrastructure.config.settings import Settings
from app.infrastructure.messaging.publishers.eventbridge_publisher import (
    EventBridgePublisher,
)
from app.infrastructure.pdf.pdf_generator import ReportLabCertificatePdfGenerator
from app.infrastructure.storage.document_storage import S3DocumentStorage
from datetime import datetime, timezone

pytestmark = pytest.mark.integration


def _settings() -> Settings:
    """Settings de prueba (no leen credenciales reales)."""
    return Settings(
        aws_region="us-east-1",
        event_bus_name="kenko-test-bus",
        documents_bucket_name="kenko-test-documents-files",
    )


async def test_s3_save_sets_key_and_content_type():
    """put_object guarda la key exacta con ContentType application/pdf."""
    with mock_aws():
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket="kenko-test-documents-files")
        storage = S3DocumentStorage(_settings())

        key = "certificates/user-1/cert-1.pdf"
        content = await ReportLabCertificatePdfGenerator().generate_affiliation_certificate_pdf(
            ProfileSnapshot(
                user_id="user-1",
                document_type="CC",
                document_number="1020304050",
                first_name="Maria Fernanda",
                last_name="Gomez Rojas",
                affiliation_start_date=datetime(2020, 6, 15, 12, 0, 0, tzinfo=timezone.utc),
            ),
            AffiliationCertificate(
                cert_id="cert-1",
                user_id="user-1",
                affiliation_start_date=datetime(2020, 6, 15, 12, 0, 0, tzinfo=timezone.utc),
                issued_at=datetime(2026, 1, 15, 12, 0, 0, tzinfo=timezone.utc),
                file_key=key,
            ),
        )
        assert await storage.save(key, content) == key

        stored = s3.get_object(Bucket="kenko-test-documents-files", Key=key)
        assert stored["ContentType"] == "application/pdf"
        assert stored["Body"].read().startswith(b"%PDF")


async def test_put_events_accepts_certificate_entry():
    """put_events acepta el entry del certificado (FailedEntryCount = 0)."""
    with mock_aws():
        bus = boto3.client("events", region_name="us-east-1")
        bus.create_event_bus(Name="kenko-test-bus")
        publisher = EventBridgePublisher(_settings())

        await publisher.publish(
            [
                events.CertificateGenerated(
                    cert_id="cert-1",
                    user_id="user-1",
                    email="maria.gomez@example.com",
                    first_name="Maria Fernanda",
                    issued_at=datetime(2026, 10, 31, 15, 0, 0, tzinfo=timezone.utc),
                    file_key="certificates/user-1/cert-1.pdf",
                    file_name="certificado-afiliacion-cert-1.pdf",
                )
            ],
            "corr-1",
        )


async def test_put_events_failure_raises_publish_error():
    """Un bus inexistente se traduce a EventPublishError (no al error boto3)."""
    with mock_aws():
        publisher = EventBridgePublisher(
            Settings(
                aws_region="us-east-1",
                event_bus_name="kenko-bus-inexistente",
                documents_bucket_name="kenko-test-documents-files",
            )
        )
        with pytest.raises(EventPublishError):
            await publisher.publish(
                [
                    events.CertificateGenerated(
                        cert_id="cert-1",
                        user_id="user-1",
                        email="maria.gomez@example.com",
                        first_name="Maria Fernanda",
                        issued_at=datetime(2026, 10, 31, 15, 0, 0, tzinfo=timezone.utc),
                        file_key="certificates/user-1/cert-1.pdf",
                        file_name="certificado-afiliacion-cert-1.pdf",
                    )
                ],
                "corr-1",
            )


def test_env_does_not_leak_into_test_settings():
    """Los settings de prueba no dependen del entorno local."""
    os.environ.pop("DOCUMENTS_BUCKET_NAME", None)
    assert _settings().documents_bucket_name == "kenko-test-documents-files"
