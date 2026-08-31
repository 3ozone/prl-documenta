"""Unit tests for JwtTokenService."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from jose import jwt

from domain.exceptions import InvalidCredentials
from infrastructure.auth.jwt_token_service import JwtTokenService


def test_create_and_decode_token_round_trip():
    svc = JwtTokenService(secret_key="test-secret")
    token = svc.create_token(email="user@test.com", role="viewer")
    payload = svc.decode_token(token)
    assert payload["sub"] == "user@test.com"
    assert payload["role"] == "viewer"


def test_decode_expired_token_raises():
    svc = JwtTokenService(secret_key="test-secret", expire_minutes=-1)
    payload = {
        "sub": "user@test.com",
        "role": "viewer",
        "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
    }
    token = jwt.encode(payload, "test-secret", algorithm="HS256")
    with pytest.raises(InvalidCredentials):
        svc.decode_token(token)


def test_decode_invalid_signature_raises():
    svc = JwtTokenService(secret_key="real-secret")
    token = svc.create_token(email="user@test.com", role="admin")
    svc_wrong = JwtTokenService(secret_key="wrong-secret")
    with pytest.raises(InvalidCredentials):
        svc_wrong.decode_token(token)
