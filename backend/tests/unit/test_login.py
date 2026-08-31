"""Unit tests for LoginUseCase."""
from __future__ import annotations

import uuid
from typing import Optional

import pytest
from passlib.context import CryptContext

from application.ports.user_repository import AbstractUserRepository
from application.use_cases.login_user import LoginCommand, LoginUseCase
from domain.entities.user import User, UserRole
from domain.exceptions import InactiveUser, InvalidCredentials
from infrastructure.auth.jwt_token_service import JwtTokenService

_pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


class InMemoryUserRepository(AbstractUserRepository):
    def __init__(self, users: list[User]):
        self._store = {u.email: u for u in users}

    def save(self, user: User) -> User:
        self._store[user.email] = user
        return user

    def get_by_email(self, email: str) -> Optional[User]:
        return self._store.get(email)

    def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        return next((u for u in self._store.values() if u.id == user_id), None)

    def exists_any_admin(self) -> bool:
        return any(u.role == UserRole.ADMIN for u in self._store.values())


def _active_user(password: str = "secret") -> User:
    return User(
        id=uuid.uuid4(),
        email="user@test.com",
        hashed_password=_pwd_ctx.hash(password),
        role=UserRole.VIEWER,
        is_active=True,
    )


def _inactive_user(password: str = "secret") -> User:
    return User(
        id=uuid.uuid4(),
        email="inactive@test.com",
        hashed_password=_pwd_ctx.hash(password),
        role=UserRole.VIEWER,
        is_active=False,
    )


def test_login_returns_token_for_valid_credentials():
    user = _active_user()
    repo = InMemoryUserRepository([user])
    use_case = LoginUseCase(repo=repo, password_hasher=_pwd_ctx, token_service=JwtTokenService())
    token = use_case.execute(LoginCommand(email="user@test.com", password="secret"))
    assert isinstance(token, str)
    assert len(token) > 0


def test_login_raises_for_wrong_password():
    user = _active_user()
    repo = InMemoryUserRepository([user])
    use_case = LoginUseCase(repo=repo, password_hasher=_pwd_ctx, token_service=JwtTokenService())
    with pytest.raises(InvalidCredentials):
        use_case.execute(LoginCommand(email="user@test.com", password="wrong"))


def test_login_raises_for_inactive_user():
    user = _inactive_user()
    repo = InMemoryUserRepository([user])
    use_case = LoginUseCase(repo=repo, password_hasher=_pwd_ctx, token_service=JwtTokenService())
    with pytest.raises(InactiveUser):
        use_case.execute(LoginCommand(email="inactive@test.com", password="secret"))
