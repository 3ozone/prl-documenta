from __future__ import annotations
from dataclasses import dataclass
from domain.entities.document import Document
from domain.value_objects.alert_level import AlertLevel


@dataclass(frozen=True)
class DocumentAlert:
    document: Document
    level: AlertLevel
    dias_restantes: int  # negativo si ya caducado
