"""Tests for UploadWorkerDocumentUseCase."""
from __future__ import annotations

from datetime import date
from unittest.mock import MagicMock

import pytest

from application.use_cases.upload_worker_document import (
    UploadWorkerDocumentCommand,
    UploadWorkerDocumentUseCase,
)
from domain.exceptions import InvalidDocumentFormat, InvalidExpiryDate, MissingRequiredField
from domain.value_objects.worker_document_type import WorkerDocumentType


class TestUploadWorkerDocumentUseCase:
    def _make_use_case(self):
        repository = MagicMock()
        storage = MagicMock()
        storage.save.return_value = "/storage/abc123.pdf"
        repository.save_worker_document.return_value = None
        return UploadWorkerDocumentUseCase(repository=repository, storage=storage)

    def test_upload_worker_document_success(self):
        use_case = self._make_use_case()
        command = UploadWorkerDocumentCommand(
            nombre_archivo="formacion.pdf",
            formato="pdf",
            fecha_validez=date(2025, 1, 1),
            fecha_caducidad=date(2026, 1, 1),
            content=b"pdf content",
            nombre_trabajador="Juan Pérez",
            dni="12345678A",
            puesto="Operario",
            tipo_documento=WorkerDocumentType.FORMACION,
        )

        result = use_case.execute(command)

        assert result.nombre_trabajador == "Juan Pérez"
        assert result.dni == "12345678A"
        assert result.puesto == "Operario"
        assert result.tipo_documento == WorkerDocumentType.FORMACION
        use_case._repository.save_worker_document.assert_called_once()

    def test_upload_worker_document_missing_nombre_trabajador(self):
        use_case = self._make_use_case()
        command = UploadWorkerDocumentCommand(
            nombre_archivo="formacion.pdf",
            formato="pdf",
            fecha_validez=date(2025, 1, 1),
            fecha_caducidad=date(2026, 1, 1),
            content=b"pdf content",
            nombre_trabajador="",
            dni="12345678A",
            puesto="Operario",
            tipo_documento=WorkerDocumentType.FORMACION,
        )

        with pytest.raises(MissingRequiredField) as exc_info:
            use_case.execute(command)

        assert "nombre_trabajador" in str(exc_info.value)

    def test_upload_worker_document_missing_dni(self):
        use_case = self._make_use_case()
        command = UploadWorkerDocumentCommand(
            nombre_archivo="formacion.pdf",
            formato="pdf",
            fecha_validez=date(2025, 1, 1),
            fecha_caducidad=date(2026, 1, 1),
            content=b"pdf content",
            nombre_trabajador="Juan Pérez",
            dni="",
            puesto="Operario",
            tipo_documento=WorkerDocumentType.FORMACION,
        )

        with pytest.raises(MissingRequiredField) as exc_info:
            use_case.execute(command)

        assert "dni" in str(exc_info.value)

    def test_upload_worker_document_missing_tipo_documento(self):
        use_case = self._make_use_case()
        command = UploadWorkerDocumentCommand(
            nombre_archivo="formacion.pdf",
            formato="pdf",
            fecha_validez=date(2025, 1, 1),
            fecha_caducidad=date(2026, 1, 1),
            content=b"pdf content",
            nombre_trabajador="Juan Pérez",
            dni="12345678A",
            puesto="Operario",
            tipo_documento=None,  # type: ignore
        )

        with pytest.raises(MissingRequiredField) as exc_info:
            use_case.execute(command)

        assert "tipo_documento" in str(exc_info.value)

    def test_upload_worker_document_invalid_dates(self):
        use_case = self._make_use_case()
        command = UploadWorkerDocumentCommand(
            nombre_archivo="formacion.pdf",
            formato="pdf",
            fecha_validez=date(2026, 1, 1),
            fecha_caducidad=date(2025, 1, 1),
            content=b"pdf content",
            nombre_trabajador="Juan Pérez",
            dni="12345678A",
            puesto="Operario",
            tipo_documento=WorkerDocumentType.FORMACION,
        )

        with pytest.raises(InvalidExpiryDate):
            use_case.execute(command)

    def test_upload_worker_document_all_types(self):
        use_case = self._make_use_case()
        for doc_type in WorkerDocumentType:
            command = UploadWorkerDocumentCommand(
                nombre_archivo="documento.pdf",
                formato="pdf",
                fecha_validez=date(2025, 1, 1),
                fecha_caducidad=date(2026, 1, 1),
                content=b"pdf content",
                nombre_trabajador="Juan Pérez",
                dni="12345678A",
                puesto="Operario",
                tipo_documento=doc_type,
            )

            result = use_case.execute(command)

            assert result.tipo_documento == doc_type
            use_case._repository.save_worker_document.assert_called()
