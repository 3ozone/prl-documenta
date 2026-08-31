"""WorkerDocumentType value object."""
from __future__ import annotations

from enum import Enum


class WorkerDocumentType(str, Enum):
    FORMACION = "formacion"
    RECONOCIMIENTO_MEDICO = "reconocimiento_medico"
    ENTREGA_EPI = "entrega_epi"
    APTITUD_MEDICA = "aptitud_medica"
