"""Auth schemas."""
from __future__ import annotations

import uuid

from pydantic import BaseModel

from domain.entities.user import UserRole


class RegisterRequest(BaseModel):
    email: str
    password: str
    role: UserRole = UserRole.VIEWER


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    role: UserRole
