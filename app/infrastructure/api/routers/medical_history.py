"""Router de historial médico (adaptador de entrada)."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Header

from app.infrastructure.api.schemas.medical_history import (
    AddHistoryRecordRequest,
    HistoryExportResponse,
    HistoryRecordResponse,
    UpdateHistoryRecordRequest,
)
from app.infrastructure.config.composition import (
    get_add_history_record_use_case,
    get_generate_history_pdf_use_case,
    get_update_history_record_use_case,
)

router = APIRouter(prefix="/medical-history", tags=["medical-history"])


@router.post("/records", response_model=HistoryRecordResponse, status_code=201)
async def add_history_record(
    body: AddHistoryRecordRequest,
    use_case: Annotated[object, Depends(get_add_history_record_use_case)],
    x_correlation_id: Annotated[str | None, Header(alias="X-Correlation-Id")] = None,
) -> HistoryRecordResponse:
    """Agrega un registro al historial de un userId."""
    correlation_id = x_correlation_id or str(uuid.uuid4())
    # TODO: delegar al caso de uso y mapear a response.
    raise NotImplementedError


@router.put("/records/{record_id}", response_model=HistoryRecordResponse)
async def update_history_record(
    record_id: str,
    body: UpdateHistoryRecordRequest,
    use_case: Annotated[object, Depends(get_update_history_record_use_case)],
    x_correlation_id: Annotated[str | None, Header(alias="X-Correlation-Id")] = None,
) -> HistoryRecordResponse:
    """Actualiza un registro del historial."""
    correlation_id = x_correlation_id or str(uuid.uuid4())
    # TODO: delegar al caso de uso y mapear a response.
    raise NotImplementedError


@router.post("/export", response_model=HistoryExportResponse, status_code=201)
async def generate_history_pdf(
    user_id: str,
    use_case: Annotated[object, Depends(get_generate_history_pdf_use_case)],
    x_correlation_id: Annotated[str | None, Header(alias="X-Correlation-Id")] = None,
) -> HistoryExportResponse:
    """Genera el PDF del historial de un userId."""
    correlation_id = x_correlation_id or str(uuid.uuid4())
    # TODO: delegar al caso de uso y mapear a response.
    raise NotImplementedError
