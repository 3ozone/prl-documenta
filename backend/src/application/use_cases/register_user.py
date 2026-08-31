"""Register user use case."""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from application.ports.user_repository import AbstractUserRepository
from domain.entities.user import User, UserRole
from domain.exceptions import InsufficientPermissions, UserAlreadyExists


@dataclass
class RegisterUserCommand:
    email: str
    password: str
    role: UserRole
    requester: User | None
    _bypass_permissions: bool = field(default=False)


class RegisterUserUseCase:
    def __init__(self, repo: AbstractUserRepository, password_hasher) -> None:
        self._repo = repo
        self._hasher = password_hasher

    def execute(self, command: RegisterUserCommand) -> User:
        # Permission logic
        if not command._bypass_permissions:
            if command.requester is None or command.requester.role == UserRole.VIEWER:
                if command.role == UserRole.ADMIN:
                    raise InsufficientPermissions("Solo un admin puede crear admins")
                command = RegisterUserCommand(
                    email=command.email,
                    password=command.password,
                    role=UserRole.VIEWER,
                    requester=command.requester,
                    _bypass_permissions=False,
                )

        if self._repo.get_by_email(command.email) is not None:
            raise UserAlreadyExists(f"Email ya registrado: {command.email}")

        hashed = self._hasher.hash(command.password)
        user = User(
            id=uuid.uuid4(),
            email=command.email,
            hashed_password=hashed,
            role=command.role,
            is_active=True,
        )
        return self._repo.save(user)
