"""Puerto de publicación de eventos de dominio."""

from abc import ABC, abstractmethod

from app.domain import domain_events as events


class EventPublisherPort(ABC):
    """Publica eventos de dominio al bus (EventBridge). NUNCA usa boto3 aquí."""

    @abstractmethod
    async def publish_authorization_issued(self, event: events.AuthorizationIssued) -> None:
        # TODO: implementar en infrastructure/messaging/publishers
        raise NotImplementedError

    @abstractmethod
    async def publish_certificate_generated(
        self, event: events.CertificateGenerated
    ) -> None:
        # TODO: implementar en infraestructura
        raise NotImplementedError

    @abstractmethod
    async def publish_medical_history_pdf_generated(
        self, event: events.MedicalHistoryPdfGenerated
    ) -> None:
        # TODO: implementar en infraestructura
        raise NotImplementedError

    @abstractmethod
    async def publish_documents_updated(self, event: events.DocumentsUpdated) -> None:
        # TODO: implementar en infraestructura
        raise NotImplementedError
