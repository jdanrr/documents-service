"""Fakes de sistema: reloj fijo, ids secuenciales y storage en memoria."""

from datetime import datetime
from uuid import UUID, uuid5, NAMESPACE_OID

from app.application.ports.output.pdf_storage_ports import DocumentStoragePort
from app.application.ports.output.system_ports import ClockPort, IdGeneratorPort


class FixedClock(ClockPort):
    """Reloj determinista para tests."""

    def __init__(self, fixed: datetime) -> None:
        self._fixed = fixed

    def now(self) -> datetime:
        return self._fixed


class SequentialIdGenerator(IdGeneratorPort):
    """Genera ids predecibles (uuid5 secuenciales)."""

    def __init__(self, prefix: str = "test-id") -> None:
        self._prefix = prefix
        self._counter = 0

    def new_id(self) -> UUID:
        self._counter += 1
        return uuid5(NAMESPACE_OID, f"{self._prefix}-{self._counter}")


class FakeDocumentStorage(DocumentStoragePort):
    """Guarda binarios en un dict y retorna la referencia."""

    def __init__(self) -> None:
        self.items: dict[str, bytes] = {}

    async def save(self, pdf_id: str, content: bytes) -> str:
        self.items[pdf_id] = content
        return f"fake://{pdf_id}.pdf"
