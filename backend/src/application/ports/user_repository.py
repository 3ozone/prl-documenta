"""Abstract user repository port."""
from __future__ import annotations

import uuid
from abc import ABC, abstractmethod

from domain.entities.user import User


class AbstractUserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User: ...

    @abstractmethod
    def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    def get_by_id(self, user_id: uuid.UUID) -> User | None: ...

    @abstractmethod
    def exists_any_admin(self) -> bool: ...
