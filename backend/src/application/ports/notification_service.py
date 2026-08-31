from abc import ABC, abstractmethod
from domain.value_objects.document_alert import DocumentAlert


class AbstractNotificationService(ABC):
    @abstractmethod
    def notify(self, alerts: list[DocumentAlert]) -> None: ...
