"""Document status value object."""
from __future__ import annotations

from enum import Enum


class DocumentStatus(str, Enum):
    VIGENTE = "vigente"
    PROXIMA_A_CADUCAR = "proxima_a_caducar"
    CADUCADA = "caducada"
