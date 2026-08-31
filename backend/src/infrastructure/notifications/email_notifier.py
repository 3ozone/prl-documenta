import logging
from application.ports.notification_service import AbstractNotificationService
from domain.value_objects.document_alert import DocumentAlert

logger = logging.getLogger(__name__)


class EmailNotifier(AbstractNotificationService):
    def __init__(self, enabled: bool = True) -> None:
        self._enabled = enabled

    def notify(self, alerts: list[DocumentAlert]) -> None:
        if not self._enabled:
            return
        for alert in alerts:
            logger.info(
                "alert.email_stub",
                extra={
                    "document_id": str(alert.document.id),
                    "nivel": alert.level.value,
                    "dias_restantes": alert.dias_restantes,
                },
            )
