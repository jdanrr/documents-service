"""Adaptador EventBridgePublisher (único lugar con boto3 para eventos).

NOTA: la firma cambió a publish(events, correlation_id); el dispatch por tipo
se implementará cuando se haga el adaptador real (fuera de esta tarea).
"""

from app.application.ports.output.event_publisher_port import EventPublisherPort
from app.infrastructure.config.settings import Settings


class EventBridgePublisher(EventPublisherPort):
    """Publica eventos de dominio al bus único kenko-{env}-bus."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        # TODO: self._client = boto3.client("events", region_name=settings.aws_region)

    async def publish(self, events: list, correlation_id: str) -> None:
        """Arma el sobre estándar por evento y lo envía con put_events."""
        # TODO: por cada evento: build_metadata(correlation_id) + payload según
        # TODO: tipo (AuthorizationIssued/CertificateGenerated/.../DocumentsUpdated).
        # TODO: self._client.put_events(Entries=[{"Source": "kenko.documents",
        # TODO:   "DetailType": ..., "Detail": json.dumps(...),
        # TODO:   "EventBusName": self._settings.event_bus_name}])
        raise NotImplementedError
