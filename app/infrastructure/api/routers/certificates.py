"""Router de certificados de afiliación (adaptador de entrada)."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Header

from app.infrastructure.api.schemas.certificates import (
    CertificateResponse,
    GenerateCertificateRequest,
)
from app.infrastructure.config.composition import get_generate_certificate_use_case

router = APIRouter(prefix="/certificates", tags=["certificates"])


@router.post("", response_model=CertificateResponse, status_code=201)
async def generate_certificate(
    body: GenerateCertificateRequest,
    use_case: Annotated[object, Depends(get_generate_certificate_use_case)],
    x_correlation_id: Annotated[str | None, Header(alias="X-Correlation-Id")] = None,
) -> CertificateResponse:
    """Genera el certificado de afiliación para un userId."""
    correlation_id = x_correlation_id or str(uuid.uuid4())
    # TODO: delegar al caso de uso y mapear a response.
    raise NotImplementedError
