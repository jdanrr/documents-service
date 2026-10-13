"""Reloj e identificadores reales (stdlib; los fakes viven en tests)."""

import uuid
from datetime import datetime, timezone

from app.application.ports.output.system_ports import ClockPort, IdGeneratorPort


class SystemClock(ClockPort):
    """Reloj del sistema (siempre UTC)."""

    def now(self) -> datetime:
        return datetime.now(timezone.utc)


class RandomIdGenerator(IdGeneratorPort):
    """Generador aleatorio de identificadores."""

    def new_id(self) -> uuid.UUID:
        return uuid.uuid4()
