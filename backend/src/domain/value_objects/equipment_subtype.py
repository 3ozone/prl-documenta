"""EquipmentSubtype value object."""
from __future__ import annotations

from enum import Enum


class EquipmentSubtype(str, Enum):
    MANTENIMIENTO = "mantenimiento"
    INSPECCION = "inspeccion"