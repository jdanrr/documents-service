"""Router de certificados de afiliación (adaptador de entrada)."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status

from app.application.errors import EventPublishError, ProfileNotFound, StorageError
from app.application.ports.input.use_cases import (
    GenerateAffiliationCertificateCommand,
    GenerateAffiliationCertificateUseCase,
)
from app.domain.exceptions import DomainError
from app.infrastructure.api.mappers.certificates import domain_to_response
from app.infrastructure.api.schemas.certificates import CertificateResponse
from app.infrastructure.api.security import CurrentUser, get_current_user
from app.infrastructure.config.composition import get_generate_certificate_use_case

router = APIRouter(prefix="/certificates", tags=["certificates"])


@router.post("", response_model=CertificateResponse, status_code=201)
async def generate_certificate(
    user: Annotated[CurrentUser, Depends(get_current_user)],
    use_case: Annotated[
        GenerateAffiliationCertificateUseCase,
        Depends(get_generate_certificate_use_case),
    ],
    x_correlation_id: Annotated[str | None, Header(alias="X-Correlation-Id")] = None,
) -> CertificateResponse:
    """Genera el certificado de afiliación del usuario autenticado (sin body)."""
    command = GenerateAffiliationCertificateCommand(
        user_id=user.user_id,
        email=user.email,
        first_name=user.first_name,
        correlation_id=x_correlation_id or str(uuid.uuid4()),
    )
    try:
        certificate = await use_case.execute(command)
    except ProfileNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except (EventPublishError, StorageError) as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY, detail=str(error)
        )
    except DomainError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)
        )
    return domain_to_response(certificate)
