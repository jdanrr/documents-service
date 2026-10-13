"""Fake del puerto de publicación (guarda eventos para aserciones)."""

from app.application.ports.output.event_publisher_port import EventPublisherPort


class FakeEventPublisher(EventPublisherPort):
    """Registra (eventos, correlation_id) y puede simular un fallo."""

    def __init__(self) -> None:
        self.published: list[tuple[list, str]] = []
        self.fail_next: Exception | None = None

    async def publish(self, events: list, correlation_id: str) -> None:
        if self.fail_next is not None:
            error, self.fail_next = self.fail_next, None
            raise error
        self.published.append((list(events), correlation_id))

    @property
    def events(self) -> list:
        """Todos los eventos publicados, en orden."""
        return [event for batch, _ in self.published for event in batch]
