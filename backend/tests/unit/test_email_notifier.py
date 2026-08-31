"""Unit tests for EmailNotifier."""
from __future__ import annotations

import logging
from datetime import date
from uuid import uuid4

import pytest

from domain.entities.document import Document
from domain.value_objects.alert_level import AlertLevel
from domain.value_objects.document_alert import DocumentAlert
from infrastructure.notifications.email_notifier import EmailNotifier


def _make_alert() -> DocumentAlert:
    doc = Document(
        id=uuid4(),
        nombre_archivo="test.pdf",
        formato="pdf",
        fecha_validez=date(2020, 1, 1),
        fecha_caducidad=date(2026, 1, 5),
    )
    return DocumentAlert(document=doc, level=AlertLevel.ALERTA, dias_restantes=10)


def test_email_notifier_logs_info(caplog):
    notifier = EmailNotifier(enabled=True)
    alert = _make_alert()
    with caplog.at_level(logging.INFO, logger="infrastructure.notifications.email_notifier"):
        notifier.notify([alert])
    assert any("alert.email_stub" in r.message for r in caplog.records)


def test_email_notifier_disabled_no_log(caplog):
    notifier = EmailNotifier(enabled=False)
    alert = _make_alert()
    with caplog.at_level(logging.INFO, logger="infrastructure.notifications.email_notifier"):
        notifier.notify([alert])
    assert not caplog.records
