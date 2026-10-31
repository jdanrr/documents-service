"""Modelos Pydantic del data de cada evento publicado."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AuthorizationIssuedPayload(BaseModel):
    """data de AuthorizationIssued (lo consume Notifications)."""

    auth_id: str = Field(alias="authId")
    user_id: str = Field(alias="userId")
    procedure: str
    doctor: str
    location: str
    issued_at: datetime = Field(alias="issuedAt")


class CertificateFilePayload(BaseModel):
    """Referencia al PDF en S3 (Notifications lo descarga y lo adjunta)."""

    model_config = ConfigDict(populate_by_name=True)

    bucket: str
    key: str
    content_type: str = Field(alias="contentType")
    file_name: str = Field(alias="fileName")


class CertificateGeneratedPayload(BaseModel):
    """data de CertificateGenerated (lo consume Notifications)."""

    model_config = ConfigDict(populate_by_name=True)

    certificate_id: str = Field(alias="certificateId")
    user_id: str = Field(alias="userId")
    email: str
    first_name: str = Field(alias="firstName")
    issued_at: datetime = Field(alias="issuedAt")
    file: CertificateFilePayload


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
