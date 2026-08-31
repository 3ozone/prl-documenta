"""Unit tests for ExpiryDate value object."""
from datetime import date

import pytest

from domain.exceptions import InvalidExpiryDate
from domain.value_objects.expiry_date import ExpiryDate


def test_expiry_date_rejects_same_date() -> None:
    d = date(2025, 1, 1)
    with pytest.raises(InvalidExpiryDate):
        ExpiryDate(fecha_validez=d, fecha_caducidad=d)


def test_expiry_date_rejects_earlier_caducidad() -> None:
    with pytest.raises(InvalidExpiryDate):
        ExpiryDate(fecha_validez=date(2025, 6, 1), fecha_caducidad=date(2025, 1, 1))


def test_expiry_date_accepts_valid_dates() -> None:
    expiry = ExpiryDate(fecha_validez=date(2025, 1, 1), fecha_caducidad=date(2025, 12, 31))
    assert expiry.fecha_caducidad > expiry.fecha_validez
