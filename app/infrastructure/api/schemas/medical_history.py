"""Schemas de historial médico (Pydantic v2, solo capa API)."""

from datetime import datetime

from pydantic import BaseModel, Field


class AddHistoryRecordRequest(BaseModel):
    """Body para agregar un registro."""

    user_id: str = Field(alias="userId")
    category: str
    description: str


class UpdateHistoryRecordRequest(BaseModel):
    """Body para actualizar un registro."""

    category: str
    description: str


class HistoryRecordResponse(BaseModel):
    """Respuesta de un registro."""

    record_id: str = Field(alias="recordId")
    user_id: str = Field(alias="userId")
    category: str
    description: str
    added_at: datetime = Field(alias="addedAt")
    updated_at: datetime = Field(alias="updatedAt")


class HistoryExportResponse(BaseModel):
    """Respuesta de una exportación a PDF."""

    pdf_id: str = Field(alias="pdfId")
    user_id: str = Field(alias="userId")
    record_count: int = Field(alias="recordCount")
    generated_at: datetime = Field(alias="generatedAt")
