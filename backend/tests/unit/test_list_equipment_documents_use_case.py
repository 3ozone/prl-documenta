"""Tests for ListEquipmentDocumentsUseCase."""
from __future__ import annotations

from datetime import date
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from application.use_cases.list_equipment_documents import (
    ListEquipmentDocumentsCommand,
    ListEquipmentDocumentsUseCase,
)
from domain.entities.document import Document


class TestListEquipmentDocumentsUseCase:
    def _make_use_case(self):
        repository = MagicMock()
        return ListEquipmentDocumentsUseCase(repository=repository)

    def test_list_equipment_documents_pagination(self):
        use_case = self._make_use_case()
        doc1 = Document(
            id=uuid4(),
            nombre_archivo="equipo1.pdf",
            formato="pdf",
            fecha_validez=date(2025, 1, 1),
            fecha_caducidad=date(2026, 1, 1),
            categoria="equipos",
            id_equipo="EQ001",
            nombre_equipo="Montacargas",
        )
        doc2 = Document(
            id=uuid4(),
            nombre_archivo="equipo2.pdf",
            formato="pdf",
            fecha_validez=date(2025, 1, 1),
            fecha_caducidad=date(2026, 1, 1),
            categoria="equipos",
            id_equipo="EQ002",
            nombre_equipo="Carretilla",
        )
        use_case._repository.get_equipment_documents.return_value = ([doc1, doc2], 2)

        result = use_case.execute(ListEquipmentDocumentsCommand(id_equipo=None, page=1, per_page=20))

        assert len(result.documents) == 2
        assert result.total == 2
        assert result.page == 1
        assert result.per_page == 20
        use_case._repository.get_equipment_documents.assert_called_once_with(id_equipo=None, page=1, per_page=20)

    def test_list_equipment_documents_filter_by_id_equipo(self):
        use_case = self._make_use_case()
        doc = Document(
            id=uuid4(),
            nombre_archivo="equipo1.pdf",
            formato="pdf",
            fecha_validez=date(2025, 1, 1),
            fecha_caducidad=date(2026, 1, 1),
            categoria="equipos",
            id_equipo="EQ001",
            nombre_equipo="Montacargas",
        )
        use_case._repository.get_equipment_documents.return_value = ([doc], 1)

        result = use_case.execute(ListEquipmentDocumentsCommand(id_equipo="EQ001", page=1, per_page=20))

        assert len(result.documents) == 1
        assert result.documents[0].id_equipo == "EQ001"
        use_case._repository.get_equipment_documents.assert_called_once_with(id_equipo="EQ001", page=1, per_page=20)

    def test_list_equipment_documents_all_fields(self):
        use_case = self._make_use_case()
        doc = Document(
            id=uuid4(),
            nombre_archivo="mantenimiento.pdf",
            formato="pdf",
            fecha_validez=date(2025, 1, 1),
            fecha_caducidad=date(2026, 1, 1),
            categoria="equipos",
            id_equipo="EQ001",
            nombre_equipo="Montacargas",
            numero_serie="SN12345",
            ubicacion="Almacén A",
            subtipo="mantenimiento",
            tipo_mantenimiento="preventivo",
            empresa_mantenedora="Mantenes S.L.",
            fecha_proximo_mantenimiento=date(2026, 6, 1),
            organismo_inspector=None,
            resultado_inspeccion=None,
            fecha_proxima_inspeccion=None,
        )
        use_case._repository.get_equipment_documents.return_value = ([doc], 1)

        result = use_case.execute(ListEquipmentDocumentsCommand(id_equipo=None, page=1, per_page=20))

        assert len(result.documents) == 1
        retrieved = result.documents[0]
        assert retrieved.id_equipo == "EQ001"
        assert retrieved.nombre_equipo == "Montacargas"
        assert retrieved.numero_serie == "SN12345"
        assert retrieved.ubicacion == "Almacén A"
        assert retrieved.subtipo == "mantenimiento"
        assert retrieved.tipo_mantenimiento == "preventivo"
        assert retrieved.empresa_mantenedora == "Mantenes S.L."