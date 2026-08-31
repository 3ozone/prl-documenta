"""Tests for UploadCompanyDocumentUseCase."""
from __future__ import annotations

from datetime import date
from unittest.mock import MagicMock

import pytest

from application.use_cases.upload_company_document import (
    UploadCompanyDocumentCommand,
    UploadCompanyDocumentUseCase,
)
from domain.exceptions import InvalidDocumentFormat, InvalidExpiryDate, MissingRequiredField


class TestUploadCompanyDocumentUseCase:
    def _make_use_case(self):
        repository = MagicMock()
        storage = MagicMock()
        storage.save.return_value = "/storage/abc123.pdf"
        repository.save_company_document.return_value = None
        return UploadCompanyDocumentUseCase(repository=repository, storage=storage)

    def test_upload_company_document_success(self):
        use_case = self._make_use_case()
        command = UploadCompanyDocumentCommand(
            nombre_archivo="certificado_aeat.pdf",
            formato="pdf",
            fecha_validez=date(2025, 1, 1),
            fecha_caducidad=date(2026, 1, 1),
            content=b"pdf content",
            razon_social="Acme SL",
            cif="A12345678",
            actividad_economica="Construcción",
            centro_trabajo="Madrid",
        )

        result = use_case.execute(command)

        assert result.razon_social == "Acme SL"
        assert result.cif == "A12345678"
        assert result.actividad_economica == "Construcción"
        assert result.centro_trabajo == "Madrid"
        use_case._repository.save_company_document.assert_called_once()

    def test_upload_company_document_missing_razon_social(self):
        use_case = self._make_use_case()
        command = UploadCompanyDocumentCommand(
            nombre_archivo="certificado_aeat.pdf",
            formato="pdf",
            fecha_validez=date(2025, 1, 1),
            fecha_caducidad=date(2026, 1, 1),
            content=b"pdf content",
            razon_social="",
            cif="A12345678",
        )

        with pytest.raises(MissingRequiredField) as exc_info:
            use_case.execute(command)

        assert "razon_social" in str(exc_info.value)

    def test_upload_company_document_missing_cif(self):
        use_case = self._make_use_case()
        command = UploadCompanyDocumentCommand(
            nombre_archivo="certificado_aeat.pdf",
            formato="pdf",
            fecha_validez=date(2025, 1, 1),
            fecha_caducidad=date(2026, 1, 1),
            content=b"pdf content",
            razon_social="Acme SL",
            cif="",
        )

        with pytest.raises(MissingRequiredField) as exc_info:
            use_case.execute(command)

        assert "cif" in str(exc_info.value)

    def test_upload_company_document_invalid_dates(self):
        use_case = self._make_use_case()
        command = UploadCompanyDocumentCommand(
            nombre_archivo="certificado_aeat.pdf",
            formato="pdf",
            fecha_validez=date(2026, 1, 1),
            fecha_caducidad=date(2025, 1, 1),
            content=b"pdf content",
            razon_social="Acme SL",
            cif="A12345678",
        )

        with pytest.raises(InvalidExpiryDate):
            use_case.execute(command)