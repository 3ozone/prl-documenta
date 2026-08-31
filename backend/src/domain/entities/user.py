"""User entity and role enum."""
from __future__ import annotations

import uuid
from dataclasses import dataclass
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    VIEWER = "viewer"


@dataclass(frozen=True)
class User:
    id: uuid.UUID
    email: str
    hashed_password: str
    role: UserRole
    is_active: bool
