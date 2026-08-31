"""MaintenanceType value object."""
from __future__ import annotations

from enum import Enum


class MaintenanceType(str, Enum):
    PREVENTIVO = "preventivo"
    CORRECTIVO = "correctivo"