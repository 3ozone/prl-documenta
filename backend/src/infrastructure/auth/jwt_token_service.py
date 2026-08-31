"""JWT token service."""
from __future__ import annotations

import logging
import os
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from domain.exceptions import InvalidCredentials

logger = logging.getLogger(__name__)


class JwtTokenService:
    def __init__(
        self,
        secret_key: str | None = None,
        algorithm: str = "HS256",
        expire_minutes: int = 60,
    ) -> None:
        self._secret = secret_key or os.environ.get("JWT_SECRET_KEY", "dev-secret-change-me")
        self._algorithm = algorithm
        self._expire_minutes = expire_minutes

    def create_token(self, email: str, role: str) -> str:
        payload = {
            "sub": email,
            "role": role,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=self._expire_minutes),
        }
        return jwt.encode(payload, self._secret, algorithm=self._algorithm)

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, self._secret, algorithms=[self._algorithm])
        except JWTError as exc:
            raise InvalidCredentials("Token inválido o expirado") from exc
