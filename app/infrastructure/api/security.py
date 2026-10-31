"""Seguridad JWT (solo infraestructura): valida el token y expone el usuario actual.

El JWT (HS256, secreto compartido) trae los claims userId, firstName y email.
El token y el secreto NUNCA se imprimen en logs; el email se enmascara.
"""

import logging
from dataclasses import dataclass
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.infrastructure.config.composition import get_settings
from app.infrastructure.config.settings import Settings

logger = logging.getLogger(__name__)

_bearer = HTTPBearer(auto_error=False)


@dataclass(frozen=True)
class CurrentUser:
    """Usuario autenticado (claims del JWT, no entra al dominio)."""

    user_id: str
    email: str
    first_name: str


def _mask_email(email: str) -> str:
    """Enmascara el email para los logs (p. ej. ma***@gmail.com)."""
    local, _, domain = email.partition("@")
    if not domain:
        return "***"
    visible = local[:2] if len(local) > 2 else local[:1]
    return f"{visible}***@{domain}"


def _unauthorized(detail: str) -> HTTPException:
    """401 sin exponer el motivo exacto al cliente."""
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> CurrentUser:
    """Valida el Bearer JWT y retorna sus claims (401 si falta o es inválido)."""
    if credentials is None or not credentials.credentials:
        raise _unauthorized("Falta el token de autenticación.")
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret,
            algorithms=["HS256"],
            options={"require": ["exp"]},
        )
    except jwt.PyJWTError:
        raise _unauthorized("Token inválido o expirado.")
    try:
        user_id = payload["userId"]
        email = payload["email"]
        first_name = payload["firstName"]
    except KeyError:
        raise _unauthorized("Token inválido o expirado.")
    if not all(isinstance(v, str) and v.strip() for v in (user_id, email, first_name)):
        raise _unauthorized("Token inválido o expirado.")
    logger.debug("Petición autenticada de %s", _mask_email(email))
    return CurrentUser(user_id=user_id, email=email, first_name=first_name)
