"""Sobre estándar EventBridge (source + detail-type + detail)."""

import json
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

from app.infrastructure.messaging.contracts.metadata import EventMetadata

PayloadT = TypeVar("PayloadT", bound=BaseModel)


class EventDetail(BaseModel, Generic[PayloadT]):
    """Contenido de detail: metadata + data."""

    model_config = ConfigDict(populate_by_name=True)

    metadata: EventMetadata
    data: PayloadT


class EventEnvelope(BaseModel, Generic[PayloadT]):
    """Sobre completo que se publica al bus único kenko-{env}-bus."""

    model_config = ConfigDict(populate_by_name=True)

    source: str = "kenko.documents"
    detail_type: str = Field(alias="detail-type")
    detail: EventDetail[PayloadT]

    def to_eventbridge_entry(self, bus_name: str) -> dict:
        """Convierte el sobre a parámetros de PutEvents."""
        detail = self.detail.model_dump(mode="json", by_alias=True)
        return {
            "Source": self.source,
            "DetailType": self.detail_type,
            "Detail": json.dumps(_with_z_suffix(detail)),
            "EventBusName": bus_name,
        }


def _with_z_suffix(value: Any) -> Any:
    """Reescribe instantes UTC con sufijo Z (2026-10-31T15:00:00Z)."""
    if isinstance(value, dict):
        return {key: _with_z_suffix(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_with_z_suffix(item) for item in value]
    if isinstance(value, str) and value.endswith("+00:00"):
        return value[:-6] + "Z"
    return value
