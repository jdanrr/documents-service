"""Adaptador EventBridgePublisher (único lugar con boto3 para eventos)."""

import json

import boto3

from app.application.ports.output.event_publisher_port import EventPublisherPort
from app.domain import domain_events as events
from app.infrastructure.config.settings import Settings
from app.infrastructure.messaging.contracts import envelope as envelope_mod
from app.infrastructure.messaging.contracts import events as payloads
from app.infrastructure.messaging.contracts.metadata import build_metadata


class EventBridgePublisher(EventPublisherPort):
    """Publica eventos de dominio al bus único kenko-{env}-bus."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        # TODO: self._client = boto3.client("events", region_name=settings.aws_region)

    def _put(self, detail_type: str, payload: dict, correlation_id: str) -> None:
        """Arma el sobre estándar y lo envía con put_events."""
        # TODO: metadata = build_metadata(correlation_id)
        # TODO: envelope = {"source": "kenko.documents", "detail-type": detail_type,
        # TODO:             "detail": {"metadata": ..., "data": payload}}
        # TODO: self._client.put_events(Entries=[{"Source": ..., "DetailType": ...,
        # TODO:                                 "Detail": json.dumps(envelope["detail"]),
        # TODO:                                 "EventBusName": self._settings.event_bus_name}])
        raise NotImplementedError

    async def publish_authorization_issued(self, event: events.AuthorizationIssued) -> None:
        # TODO: mapear evento dominio -> AuthorizationIssuedPayload y llamar _put("AuthorizationIssued", ...).
        raise NotImplementedError

    async def publish_certificate_generated(
        self, event: events.CertificateGenerated
    ) -> None:
        # TODO: mapear a CertificateGeneratedPayload y _put("CertificateGenerated", ...).
        raise NotImplementedError

    async def publish_medical_history_pdf_generated(
        self, event: events.MedicalHistoryPdfGenerated
    ) -> None:
        # TODO: mapear a MedicalHistoryPdfGeneratedPayload y _put("MedicalHistoryPdfGenerated", ...).
        raise NotImplementedError

    async def publish_documents_updated(self, event: events.DocumentsUpdated) -> None:
        # TODO: mapear a DocumentsUpdatedPayload y _put("DocumentsUpdated", ...).
        raise NotImplementedError
