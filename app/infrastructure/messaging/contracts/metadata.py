"""Builder de metadata del sobre estándar (eventId UUIDv7 + correlationId)."""

import secrets
import uuid
from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field


class EventMetadata(BaseModel):
    """Bloque metadata dentro de detail."""

    model_config = ConfigDict(populate_by_name=True)

    event_id: str = Field(alias="eventId")
    event_version: str = Field(default="1", alias="eventVersion")
    occurred_at: datetime = Field(alias="occurredAt")
    correlation_id: str = Field(alias="correlationId")


def _new_uuid7() -> uuid.UUID:
    """Genera un UUID v7 (timestamp en ms + aleatorio, RFC 9562).

    Python 3.11 no trae uuid7 en la librería estándar; esta función mínima
    evita agregar una dependencia solo para el eventId.
    """
    unix_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    rand_a = secrets.randbits(12)
    rand_b = secrets.randbits(62)
    value = (unix_ms << 80) | (0x7 << 76) | (rand_a << 64) | (0b10 << 62) | rand_b
    return uuid.UUID(int=value)


def build_metadata(correlation_id: str | None = None) -> EventMetadata:
    """Crea la metadata: genera eventId UUIDv7 y reutiliza o genera correlationId."""
    return EventMetadata(
        event_id=str(_new_uuid7()),
        occurred_at=datetime.now(timezone.utc),
        correlation_id=correlation_id or str(uuid.uuid4()),
    )
