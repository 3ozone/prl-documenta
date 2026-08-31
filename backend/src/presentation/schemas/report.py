"""Report schemas."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class ReportStatusQuery(BaseModel):
    formato: str
    categoria: str | None = None


class ReportStatusResponse(BaseModel):
    generated_at: datetime
