"""Adaptador EventBridgePublisher (único lugar con boto3 para eventos)."""

import boto3

from app.application.errors import EventPublishError
from app.application.ports.output.event_publisher_port import EventPublisherPort
from app.domain import domain_events as domain
from app.infrastructure.config.settings import Settings
from app.infrastructure.messaging.contracts.envelope import EventDetail, EventEnvelope
from app.infrastructure.messaging.contracts.events import (
    CertificateFilePayload,
    CertificateGeneratedPayload,
)
from app.infrastructure.messaging.contracts.metadata import build_metadata


class EventBridgePublisher(EventPublisherPort):
    """Publica eventos de dominio al bus único kenko-{env}-bus."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client = boto3.client("events", region_name=settings.aws_region)

    async def publish(self, events: list, correlation_id: str) -> None:
        """Arma el sobre estándar por evento y lo envía con put_events."""
        try:
            response = self._client.put_events(
                Entries=[self._to_entry(event, correlation_id) for event in events]
            )
        except Exception as error:
            raise EventPublishError() from error
        if response.get("FailedEntryCount", 0):
            raise EventPublishError("EventBridge rechazó uno o más eventos.")

    def _to_entry(self, event: object, correlation_id: str) -> dict:
        """Convierte un evento de dominio a parámetros de PutEvents."""
        if isinstance(event, domain.CertificateGenerated):
            payload = CertificateGeneratedPayload(
                certificate_id=event.cert_id,
                user_id=event.user_id,
                email=event.email,
                first_name=event.first_name,
                issued_at=event.issued_at,
                file=CertificateFilePayload(
                    bucket=self._settings.documents_bucket_name,
                    key=event.file_key,
                    content_type="application/pdf",
                    file_name=event.file_name,
                ),
            )
            envelope: EventEnvelope[CertificateGeneratedPayload] = EventEnvelope(
                detail_type="CertificateGenerated",
                detail=EventDetail(
                    metadata=build_metadata(correlation_id), data=payload
                ),
            )
            return envelope.to_eventbridge_entry(self._settings.event_bus_name)
        # Otros detail-type pertenecen a otros features (fuera de alcance).
        raise NotImplementedError(f"Evento no soportado: {type(event).__name__}.")
