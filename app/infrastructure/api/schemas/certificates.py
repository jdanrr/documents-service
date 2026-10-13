"""Schemas de certificados de afiliación (Pydantic v2, solo capa API)."""

from datetime import datetime

from pydantic import BaseModel, Field


class GenerateCertificateRequest(BaseModel):
    """Body para generar un certificado."""

    user_id: str = Field(alias="userId")


class CertificateResponse(BaseModel):
    """Respuesta de un certificado."""

    cert_id: str = Field(alias="certId")
    user_id: str = Field(alias="userId")
    issued_at: datetime = Field(alias="issuedAt")
    status: str
