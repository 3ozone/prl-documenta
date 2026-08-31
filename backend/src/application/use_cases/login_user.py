"""Login user use case."""
from __future__ import annotations

from dataclasses import dataclass

from application.ports.user_repository import AbstractUserRepository
from domain.exceptions import InactiveUser, InvalidCredentials


@dataclass
class LoginCommand:
    email: str
    password: str


class LoginUseCase:
    def __init__(self, repo: AbstractUserRepository, password_hasher, token_service) -> None:
        self._repo = repo
        self._hasher = password_hasher
        self._token_service = token_service

    def execute(self, command: LoginCommand) -> str:
        user = self._repo.get_by_email(command.email)
        if user is None:
            raise InvalidCredentials("Credenciales inválidas")

        if not self._hasher.verify(command.password, user.hashed_password):
            raise InvalidCredentials("Credenciales inválidas")

        if not user.is_active:
            raise InactiveUser("Usuario inactivo")

        return self._token_service.create_token(email=user.email, role=user.role.value)
