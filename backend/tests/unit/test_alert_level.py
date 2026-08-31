"""Unit tests for AlertLevel and CheckExpiryUseCase._compute_level."""
from __future__ import annotations

from datetime import date
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from application.use_cases.check_expiry import CheckExpiryUseCase
from domain.value_objects.alert_level import AlertLevel
from domain.entities.document import Document


def _make_doc(fecha_caducidad: date) -> Document:
    return Document(
        id=uuid4(),
        nombre_archivo="test.pdf",
        formato="pdf",
        fecha_validez=date(2020, 1, 1),
        fecha_caducidad=fecha_caducidad,
    )


def test_alert_level_expired():
    assert CheckExpiryUseCase._compute_level(0) == AlertLevel.CADUCADA
    assert CheckExpiryUseCase._compute_level(-1) == AlertLevel.CADUCADA


def test_alert_level_critica():
    assert CheckExpiryUseCase._compute_level(1) == AlertLevel.ALERTA_CRITICA
    assert CheckExpiryUseCase._compute_level(5) == AlertLevel.ALERTA_CRITICA


def test_alert_level_alerta():
    assert CheckExpiryUseCase._compute_level(6) == AlertLevel.ALERTA
    assert CheckExpiryUseCase._compute_level(15) == AlertLevel.ALERTA


def test_alert_level_aviso():
    assert CheckExpiryUseCase._compute_level(16) == AlertLevel.AVISO
    assert CheckExpiryUseCase._compute_level(30) == AlertLevel.AVISO


def test_alert_level_ok():
    assert CheckExpiryUseCase._compute_level(31) == AlertLevel.OK


def test_check_expiry_uses_reference_date():
    ref = date(2026, 1, 1)
    doc = _make_doc(fecha_caducidad=date(2026, 1, 10))  # 9 days → ALERTA
    mock_repo = MagicMock()
    mock_repo.get_expiring_documents.return_value = [doc]

    use_case = CheckExpiryUseCase(mock_repo)
    alerts = use_case.execute(fecha_referencia=ref)

    mock_repo.get_expiring_documents.assert_called_once_with(days_ahead=30, fecha=ref)
    assert len(alerts) == 1
    assert alerts[0].level == AlertLevel.ALERTA
    assert alerts[0].dias_restantes == 9
