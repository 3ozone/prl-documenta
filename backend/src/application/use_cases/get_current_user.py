"""Get current user use case."""
from __future__ import annotations

from application.ports.user_repository import AbstractUserRepository
from domain.entities.user import User
from domain.exceptions import InvalidCredentials


class GetCurrentUserUseCase:
    def __init__(self, repo: AbstractUserRepository, token_service) -> None:
        self._repo = repo
        self._token_service = token_service

    def execute(self, token: str) -> User:
        try:
            payload = self._token_service.decode_token(token)
            email: str = payload["sub"]
        except (InvalidCredentials, KeyError) as exc:
            raise InvalidCredentials("Token inválido") from exc

        user = self._repo.get_by_email(email)
        if user is None:
            raise InvalidCredentials("Usuario no encontrado")
        return user
