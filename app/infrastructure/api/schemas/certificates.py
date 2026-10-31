"""Schemas de certificados de afiliación (Pydantic v2, solo capa API)."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CertificateResponse(BaseModel):
    """Respuesta de un certificado generado."""

    model_config = ConfigDict(populate_by_name=True)

    certificate_id: str = Field(alias="certificateId")
    issued_at: datetime = Field(alias="issuedAt")
    affiliation_start_date: datetime = Field(alias="affiliationStartDate")
