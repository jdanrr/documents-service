"""Fakes de sistema: reloj fijo, ids secuenciales y storage en memoria."""

from datetime import datetime
from uuid import UUID, uuid5, NAMESPACE_OID

from app.application.errors import StorageError
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
        self.fail_next: Exception | None = None

    async def save(
        self, key: str, content: bytes, content_type: str = "application/pdf"
    ) -> str:
        if self.fail_next is not None:
            error, self.fail_next = self.fail_next, None
            raise error
        self.items[key] = content
        return f"fake://{key}"

    def fail_with_storage_error(self) -> None:
        """Programa un fallo de subida (StorageError)."""
        self.fail_next = StorageError("subida fallida")
