"""Schemas de autorizaciones (Pydantic v2, solo capa API)."""

from datetime import datetime

from pydantic import BaseModel, Field


class IssueAuthorizationRequest(BaseModel):
    """Body para emitir una autorización."""

    user_id: str = Field(alias="userId")
    procedure: str
    doctor: str
    location: str


class AuthorizationResponse(BaseModel):
    """Respuesta de una autorización."""

    auth_id: str = Field(alias="authId")
    user_id: str = Field(alias="userId")
    procedure: str
    doctor: str
    location: str
    issued_at: datetime = Field(alias="issuedAt")
    status: str
