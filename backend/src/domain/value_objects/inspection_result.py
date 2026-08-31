"""InspectionResult value object."""
from __future__ import annotations

from enum import Enum


class InspectionResult(str, Enum):
    FAVORABLE = "favorable"
    CONDICIONADO = "condicionado"
    DESFAVORABLE = "desfavorable"