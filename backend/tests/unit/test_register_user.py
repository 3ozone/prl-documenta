"""Unit tests for RegisterUserUseCase."""
from __future__ import annotations

import uuid
from typing import Optional

import pytest
from passlib.context import CryptContext

from application.ports.user_repository import AbstractUserRepository
from application.use_cases.register_user import RegisterUserCommand, RegisterUserUseCase
from domain.entities.user import User, UserRole
from domain.exceptions import InsufficientPermissions, UserAlreadyExists

_pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


class InMemoryUserRepository(AbstractUserRepository):
    def __init__(self):
        self._store: dict[str, User] = {}

    def save(self, user: User) -> User:
        self._store[user.email] = user
        return user

    def get_by_email(self, email: str) -> Optional[User]:
        return self._store.get(email)

    def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        return next((u for u in self._store.values() if u.id == user_id), None)

    def exists_any_admin(self) -> bool:
        return any(u.role == UserRole.ADMIN for u in self._store.values())


def _make_use_case(repo=None):
    if repo is None:
        repo = InMemoryUserRepository()
    return RegisterUserUseCase(repo=repo, password_hasher=_pwd_ctx), repo


def _make_admin() -> User:
    return User(
        id=uuid.uuid4(),
        email="admin@test.com",
        hashed_password=_pwd_ctx.hash("pass"),
        role=UserRole.ADMIN,
        is_active=True,
    )


def _make_viewer() -> User:
    return User(
        id=uuid.uuid4(),
        email="viewer@test.com",
        hashed_password=_pwd_ctx.hash("pass"),
        role=UserRole.VIEWER,
        is_active=True,
    )


def test_register_creates_viewer_without_requester():
    use_case, _ = _make_use_case()
    user = use_case.execute(
        RegisterUserCommand(email="u@test.com", password="pass", role=UserRole.VIEWER, requester=None)
    )
    assert user.role == UserRole.VIEWER
    assert user.email == "u@test.com"


def test_register_admin_requires_admin_requester():
    """An admin requester can create an admin."""
    use_case, _ = _make_use_case()
    admin = _make_admin()
    user = use_case.execute(
        RegisterUserCommand(
            email="new_admin@test.com",
            password="pass",
            role=UserRole.ADMIN,
            requester=admin,
            _bypass_permissions=True,
        )
    )
    assert user.role == UserRole.ADMIN


def test_register_viewer_cannot_create_admin():
    use_case, _ = _make_use_case()
    viewer = _make_viewer()
    with pytest.raises(InsufficientPermissions):
        use_case.execute(
            RegisterUserCommand(
                email="new_admin@test.com",
                password="pass",
                role=UserRole.ADMIN,
                requester=viewer,
            )
        )


def test_register_duplicate_email_raises():
    use_case, _ = _make_use_case()
    use_case.execute(
        RegisterUserCommand(email="dup@test.com", password="pass", role=UserRole.VIEWER, requester=None)
    )
    with pytest.raises(UserAlreadyExists):
        use_case.execute(
            RegisterUserCommand(email="dup@test.com", password="pass2", role=UserRole.VIEWER, requester=None)
        )


def test_register_hashes_password():
    use_case, repo = _make_use_case()
    use_case.execute(
        RegisterUserCommand(email="h@test.com", password="plaintext", role=UserRole.VIEWER, requester=None)
    )
    saved = repo.get_by_email("h@test.com")
    assert saved is not None
    assert saved.hashed_password != "plaintext"
    assert _pwd_ctx.verify("plaintext", saved.hashed_password)
