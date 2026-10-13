"""Puerto de publicación de eventos de dominio.

Un solo método: recibe la lista de eventos en orden y el correlation_id
(que viaja fuera de los eventos; el sobre lo arma la infraestructura).
"""

from abc import ABC, abstractmethod


class EventPublisherPort(ABC):
    """Publica eventos de dominio al bus (EventBridge). NUNCA usa boto3 aquí."""

    @abstractmethod
    async def publish(self, events: list, correlation_id: str) -> None:
        """Publica los eventos en el orden recibido."""
        raise NotImplementedError
