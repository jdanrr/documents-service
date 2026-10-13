"""Modelos Pydantic del data de cada evento publicado."""

from datetime import datetime

from pydantic import BaseModel, Field


class AuthorizationIssuedPayload(BaseModel):
    """data de AuthorizationIssued (lo consume Notifications)."""

    auth_id: str = Field(alias="authId")
    user_id: str = Field(alias="userId")
    procedure: str
    doctor: str
    location: str
    issued_at: datetime = Field(alias="issuedAt")


class CertificateGeneratedPayload(BaseModel):
    """data de CertificateGenerated (lo consume Notifications)."""

    cert_id: str = Field(alias="certId")
    user_id: str = Field(alias="userId")
    issued_at: datetime = Field(alias="issuedAt")


class MedicalHistoryPdfGeneratedPayload(BaseModel):
    """data de MedicalHistoryPdfGenerated (lo consume Notifications)."""

    pdf_id: str = Field(alias="pdfId")
    user_id: str = Field(alias="userId")
    record_count: int = Field(alias="recordCount")
    generated_at: datetime = Field(alias="generatedAt")


class DocumentsUpdatedPayload(BaseModel):
    """data de DocumentsUpdated (auditoría, sin consumidor por ahora)."""

    document_id: str = Field(alias="documentId")
    document_type: str = Field(alias="documentType")
    user_id: str = Field(alias="userId")
    operation: str
    updated_at: datetime = Field(alias="updatedAt")
