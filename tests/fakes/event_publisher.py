"""Fake del puerto de publicación (guarda eventos para aserciones)."""

from app.application.ports.output.event_publisher_port import EventPublisherPort
from app.domain import domain_events as events


class FakeEventPublisher(EventPublisherPort):
    """Registra los eventos publicados en listas por tipo."""

    def __init__(self) -> None:
        self.authorization_issued: list[events.AuthorizationIssued] = []
        self.certificate_generated: list[events.CertificateGenerated] = []
        self.pdf_generated: list[events.MedicalHistoryPdfGenerated] = []
        self.documents_updated: list[events.DocumentsUpdated] = []

    async def publish_authorization_issued(self, event: events.AuthorizationIssued) -> None:
        self.authorization_issued.append(event)

    async def publish_certificate_generated(self, event: events.CertificateGenerated) -> None:
        self.certificate_generated.append(event)

    async def publish_medical_history_pdf_generated(self, event: events.MedicalHistoryPdfGenerated) -> None:
        self.pdf_generated.append(event)

    async def publish_documents_updated(self, event: events.DocumentsUpdated) -> None:
        self.documents_updated.append(event)
