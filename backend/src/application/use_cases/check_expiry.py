from datetime import date
from application.ports.document_repository import AbstractDocumentRepository
from domain.value_objects.alert_level import AlertLevel
from domain.value_objects.document_alert import DocumentAlert

THRESHOLD_AVISO = 30
THRESHOLD_ALERTA = 15
THRESHOLD_ALERTA_CRITICA = 5


class CheckExpiryUseCase:
    def __init__(self, repo: AbstractDocumentRepository) -> None:
        self._repo = repo

    def execute(self, fecha_referencia: date) -> list[DocumentAlert]:
        docs = self._repo.get_expiring_documents(days_ahead=THRESHOLD_AVISO, fecha=fecha_referencia)
        alerts = []
        for doc in docs:
            dias = (doc.fecha_caducidad - fecha_referencia).days
            level = self._compute_level(dias)
            if level != AlertLevel.OK:
                alerts.append(DocumentAlert(document=doc, level=level, dias_restantes=dias))
        return sorted(alerts, key=lambda a: a.dias_restantes)

    @staticmethod
    def _compute_level(dias: int) -> AlertLevel:
        if dias <= 0:
            return AlertLevel.CADUCADA
        if dias <= THRESHOLD_ALERTA_CRITICA:
            return AlertLevel.ALERTA_CRITICA
        if dias <= THRESHOLD_ALERTA:
            return AlertLevel.ALERTA
        if dias <= THRESHOLD_AVISO:
            return AlertLevel.AVISO
        return AlertLevel.OK
