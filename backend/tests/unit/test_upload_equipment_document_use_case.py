"""Tests for UploadEquipmentDocumentUseCase."""
from __future__ import annotations

from datetime import date
from unittest.mock import MagicMock

import pytest

from application.use_cases.upload_equipment_document import (
    UploadEquipmentDocumentCommand,
    UploadEquipmentDocumentUseCase,
)
from domain.exceptions import InvalidDocumentFormat, InvalidExpiryDate, MissingRequiredField
from domain.value_objects.equipment_subtype import EquipmentSubtype
from domain.value_objects.maintenance_type import MaintenanceType
from domain.value_objects.inspection_result import InspectionResult


class TestUploadEquipmentDocumentUseCase:
    def _make_use_case(self):
        repository = MagicMock()
        storage = MagicMock()
        storage.save.return_value = "/storage/abc123.pdf"
        repository.save_equipment_document.return_value = None
        return UploadEquipmentDocumentUseCase(repository=repository, storage=storage)

    def test_upload_equipment_document_success(self):
        use_case = self._make_use_case()
        command = UploadEquipmentDocumentCommand(
            nombre_archivo="equipo.pdf",
            formato="pdf",
            fecha_validez=date(2025, 1, 1),
            fecha_caducidad=date(2026, 1, 1),
            content=b"pdf content",
            id_equipo="EQ001",
            nombre_equipo="Montacargas",
            numero_serie="SN12345",
            ubicacion="Almacén A",
        )

        result = use_case.execute(command)

        assert result.id_equipo == "EQ001"
        assert result.nombre_equipo == "Montacargas"
        assert result.numero_serie == "SN12345"
        assert result.ubicacion == "Almacén A"
        use_case._repository.save_equipment_document.assert_called_once()

    def test_upload_equipment_document_missing_id_equipo(self):
        use_case = self._make_use_case()
        command = UploadEquipmentDocumentCommand(
            nombre_archivo="equipo.pdf",
            formato="pdf",
            fecha_validez=date(2025, 1, 1),
            fecha_caducidad=date(2026, 1, 1),
            content=b"pdf content",
            id_equipo="",
            nombre_equipo="Montacargas",
        )

        with pytest.raises(MissingRequiredField) as exc_info:
            use_case.execute(command)

        assert "id_equipo" in str(exc_info.value)

    def test_upload_equipment_document_missing_nombre_equipo(self):
        use_case = self._make_use_case()
        command = UploadEquipmentDocumentCommand(
            nombre_archivo="equipo.pdf",
            formato="pdf",
            fecha_validez=date(2025, 1, 1),
            fecha_caducidad=date(2026, 1, 1),
            content=b"pdf content",
            id_equipo="EQ001",
            nombre_equipo="",
        )

        with pytest.raises(MissingRequiredField) as exc_info:
            use_case.execute(command)

        assert "nombre_equipo" in str(exc_info.value)

    def test_upload_equipment_document_maintenance_subtype_success(self):
        use_case = self._make_use_case()
        command = UploadEquipmentDocumentCommand(
            nombre_archivo="mantenimiento.pdf",
            formato="pdf",
            fecha_validez=date(2025, 1, 1),
            fecha_caducidad=date(2026, 1, 1),
            content=b"pdf content",
            id_equipo="EQ001",
            nombre_equipo="Montacargas",
            subtipo=EquipmentSubtype.MANTENIMIENTO,
            tipo_mantenimiento=MaintenanceType.PREVENTIVO,
            empresa_mantenedora="Mantenes S.L.",
            fecha_proximo_mantenimiento=date(2026, 6, 1),
        )

        result = use_case.execute(command)

        assert result.subtipo == EquipmentSubtype.MANTENIMIENTO
        assert result.tipo_mantenimiento == MaintenanceType.PREVENTIVO
        assert result.empresa_mantenedora == "Mantenes S.L."
        use_case._repository.save_equipment_document.assert_called_once()

    def test_upload_equipment_document_maintenance_subtype_missing_fields(self):
        use_case = self._make_use_case()
        command = UploadEquipmentDocumentCommand(
            nombre_archivo="mantenimiento.pdf",
            formato="pdf",
            fecha_validez=date(2025, 1, 1),
            fecha_caducidad=date(2026, 1, 1),
            content=b"pdf content",
            id_equipo="EQ001",
            nombre_equipo="Montacargas",
            subtipo=EquipmentSubtype.MANTENIMIENTO,
            tipo_mantenimiento=None,
            empresa_mantenedora=None,
            fecha_proximo_mantenimiento=None,
        )

        with pytest.raises(MissingRequiredField) as exc_info:
            use_case.execute(command)

        assert "tipo_mantenimiento" in str(exc_info.value)

    def test_upload_equipment_document_inspection_subtype_success(self):
        use_case = self._make_use_case()
        command = UploadEquipmentDocumentCommand(
            nombre_archivo="inspeccion.pdf",
            formato="pdf",
            fecha_validez=date(2025, 1, 1),
            fecha_caducidad=date(2026, 1, 1),
            content=b"pdf content",
            id_equipo="EQ001",
            nombre_equipo="Montacargas",
            subtipo=EquipmentSubtype.INSPECCION,
            organismo_inspector="Inspectores S.A.",
            resultado_inspeccion=InspectionResult.FAVORABLE,
            fecha_proxima_inspeccion=date(2026, 6, 1),
        )

        result = use_case.execute(command)

        assert result.subtipo == EquipmentSubtype.INSPECCION
        assert result.organismo_inspector == "Inspectores S.A."
        assert result.resultado_inspeccion == InspectionResult.FAVORABLE
        use_case._repository.save_equipment_document.assert_called_once()

    def test_upload_equipment_document_inspection_subtype_missing_fields(self):
        use_case = self._make_use_case()
        command = UploadEquipmentDocumentCommand(
            nombre_archivo="inspeccion.pdf",
            formato="pdf",
            fecha_validez=date(2025, 1, 1),
            fecha_caducidad=date(2026, 1, 1),
            content=b"pdf content",
            id_equipo="EQ001",
            nombre_equipo="Montacargas",
            subtipo=EquipmentSubtype.INSPECCION,
            organismo_inspector=None,
            resultado_inspeccion=None,
            fecha_proxima_inspeccion=None,
        )

        with pytest.raises(MissingRequiredField) as exc_info:
            use_case.execute(command)

        assert "organismo_inspector" in str(exc_info.value)

    def test_upload_equipment_document_invalid_dates(self):
        use_case = self._make_use_case()
        command = UploadEquipmentDocumentCommand(
            nombre_archivo="equipo.pdf",
            formato="pdf",
            fecha_validez=date(2026, 1, 1),
            fecha_caducidad=date(2025, 1, 1),
            content=b"pdf content",
            id_equipo="EQ001",
            nombre_equipo="Montacargas",
        )

        with pytest.raises(InvalidExpiryDate):
            use_case.execute(command)