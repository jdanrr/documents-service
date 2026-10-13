"""Router de autorizaciones médicas (adaptador de entrada)."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Header

from app.infrastructure.api.schemas.authorizations import (
    AuthorizationResponse,
    IssueAuthorizationRequest,
)
from app.infrastructure.config.composition import get_issue_authorization_use_case

router = APIRouter(prefix="/authorizations", tags=["authorizations"])


@router.post("", response_model=AuthorizationResponse, status_code=201)
async def issue_authorization(
    body: IssueAuthorizationRequest,
    use_case: Annotated[object, Depends(get_issue_authorization_use_case)],
    x_correlation_id: Annotated[str | None, Header(alias="X-Correlation-Id")] = None,
) -> AuthorizationResponse:
    """Emite una autorización médica para un userId."""
    correlation_id = x_correlation_id or str(uuid.uuid4())
    # TODO: mapear body -> caso de uso con mappers, ejecutar y mapear a response.
    raise NotImplementedError
