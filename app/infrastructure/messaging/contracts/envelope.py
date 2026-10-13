"""Sobre estándar EventBridge (source + detail-type + detail)."""

from typing import Generic, TypeVar

from pydantic import BaseModel, Field

from app.infrastructure.messaging.contracts.metadata import EventMetadata

PayloadT = TypeVar("PayloadT", bound=BaseModel)


class EventDetail(BaseModel, Generic[PayloadT]):
    """Contenido de detail: metadata + data."""

    metadata: EventMetadata
    data: PayloadT


class EventEnvelope(BaseModel, Generic[PayloadT]):
    """Sobre completo que se publica al bus único kenko-{env}-bus."""

    source: str = "kenko.documents"
    detail_type: str = Field(alias="detail-type")
    detail: EventDetail[PayloadT]
    # TODO: método to_eventbridge_entry(bus_name) -> dict con Source/DetailType/Detail/EventBusName.
