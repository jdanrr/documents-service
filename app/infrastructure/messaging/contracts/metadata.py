"""Builder de metadata del sobre estándar (eventId UUIDv7 + correlationId)."""

import uuid
from datetime import datetime, timezone

from pydantic import BaseModel, Field


class EventMetadata(BaseModel):
    """Bloque metadata dentro de detail."""

    event_id: str = Field(alias="eventId")
    event_version: str = Field(default="1", alias="eventVersion")
    occurred_at: datetime = Field(alias="occurredAt")
    correlation_id: str = Field(alias="correlationId")


def build_metadata(correlation_id: str | None = None) -> EventMetadata:
    """Crea la metadata: genera eventId UUIDv7 y reutiliza o genera correlationId."""
    # TODO: usar uuid.uuid7() (Python 3.11+ no lo tiene; usar librería o uuid4 temporal).
    # TODO: occurred_at = datetime.now(timezone.utc).isoformat().
    raise NotImplementedError
