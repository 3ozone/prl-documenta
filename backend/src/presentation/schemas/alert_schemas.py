from pydantic import BaseModel
from uuid import UUID
from datetime import date
from typing import Optional


class AlertResponse(BaseModel):
    document_id: UUID
    nombre_archivo: str
    categoria: Optional[str] = None
    fecha_caducidad: date
    nivel: str
    dias_restantes: int
