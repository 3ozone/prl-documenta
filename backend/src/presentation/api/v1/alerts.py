from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Query
from domain.value_objects.alert_level import AlertLevel
from application.use_cases.check_expiry import CheckExpiryUseCase
from presentation.schemas.alert_schemas import AlertResponse
from presentation.dependencies import get_check_expiry_use_case, require_viewer_or_admin
from domain.entities.user import User

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=list[AlertResponse])
def get_alerts(
    nivel: Optional[AlertLevel] = Query(default=None),
    use_case: CheckExpiryUseCase = Depends(get_check_expiry_use_case),
    _current_user: User = Depends(require_viewer_or_admin),
) -> list[AlertResponse]:
    alerts = use_case.execute(fecha_referencia=date.today())
    if nivel is not None:
        alerts = [a for a in alerts if a.level == nivel]
    return [
        AlertResponse(
            document_id=a.document.id,
            nombre_archivo=a.document.nombre_archivo,
            categoria=a.document.categoria,
            fecha_caducidad=a.document.fecha_caducidad,
            nivel=a.level.value,
            dias_restantes=a.dias_restantes,
        )
        for a in alerts
    ]
