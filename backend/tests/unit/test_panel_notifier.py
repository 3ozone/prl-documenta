"""Unit tests for InternalPanelNotifier."""
from __future__ import annotations

from datetime import date
from uuid import uuid4

from domain.entities.document import Document
from domain.value_objects.alert_level import AlertLevel
from domain.value_objects.document_alert import DocumentAlert
from infrastructure.notifications.panel_notifier import InternalPanelNotifier


def _make_alert() -> DocumentAlert:
    doc = Document(
        id=uuid4(),
        nombre_archivo="test.pdf",
        formato="pdf",
        fecha_validez=date(2020, 1, 1),
        fecha_caducidad=date(2026, 1, 5),
    )
    return DocumentAlert(document=doc, level=AlertLevel.ALERTA, dias_restantes=10)


def test_panel_notifier_stores_alerts():
    notifier = InternalPanelNotifier(enabled=True)
    alert = _make_alert()
    notifier.notify([alert])
    result = notifier.get_alerts()
    assert len(result) == 1
    assert result[0] == alert


def test_panel_notifier_disabled_no_store():
    notifier = InternalPanelNotifier(enabled=False)
    alert = _make_alert()
    notifier.notify([alert])
    assert notifier.get_alerts() == []
