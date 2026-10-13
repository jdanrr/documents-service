"""Puertos de sistema: reloj e identificadores (determinismo en tests)."""

from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID


class ClockPort(ABC):
    """Fuente de tiempo (siempre UTC)."""

    @abstractmethod
    def now(self) -> datetime:
        """Retorna el instante actual en UTC."""
        raise NotImplementedError


class IdGeneratorPort(ABC):
    """Generador de identificadores."""

    @abstractmethod
    def new_id(self) -> UUID:
        """Genera un identificador único."""
        raise NotImplementedError
