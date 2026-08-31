from application.ports.notification_service import AbstractNotificationService
from domain.value_objects.document_alert import DocumentAlert


class InternalPanelNotifier(AbstractNotificationService):
    def __init__(self, enabled: bool = True) -> None:
        self._enabled = enabled
        self._alerts: list[DocumentAlert] = []

    def notify(self, alerts: list[DocumentAlert]) -> None:
        if not self._enabled:
            return
        self._alerts = list(alerts)

    def get_alerts(self) -> list[DocumentAlert]:
        return list(self._alerts)
