"""ExpiryDate value object."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from domain.exceptions import InvalidExpiryDate


@dataclass(frozen=True)
class ExpiryDate:
    fecha_validez: date
    fecha_caducidad: date

    def __post_init__(self) -> None:
        if self.fecha_caducidad <= self.fecha_validez:
            raise InvalidExpiryDate(
                "fecha_caducidad debe ser posterior a fecha_validez"
            )
