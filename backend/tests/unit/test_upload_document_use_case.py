"""Unit tests for UploadDocumentUseCase."""
from datetime import date
from unittest.mock import MagicMock
from uuid import UUID

import pytest

from application.use_cases.upload_document import UploadDocumentCommand, UploadDocumentUseCase
from domain.exceptions import InvalidDocumentCategory, InvalidDocumentFormat, InvalidExpiryDate


def make_use_case():
    repo = MagicMock()
    storage = MagicMock()
    storage.save.return_value = "/data/documents/some-id.pdf"
    return UploadDocumentUseCase(repository=repo, storage=storage), repo, storage


def valid_command(**kwargs) -> UploadDocumentCommand:
    defaults = dict(
        nombre_archivo="doc.pdf",
        formato="pdf",
        fecha_validez=date(2025, 1, 1),
        fecha_caducidad=date(2025, 12, 31),
        content=b"%PDF-1.4",
        categoria=None,
        uploaded_by=None,
    )
    defaults.update(kwargs)
    return UploadDocumentCommand(**defaults)


def test_rejects_non_pdf_format() -> None:
    use_case, _, _ = make_use_case()
    with pytest.raises(InvalidDocumentFormat):
        use_case.execute(valid_command(formato="docx"))


def test_rejects_invalid_expiry() -> None:
    use_case, _, _ = make_use_case()
    with pytest.raises(InvalidExpiryDate):
        use_case.execute(valid_command(fecha_validez=date(2025, 6, 1), fecha_caducidad=date(2025, 1, 1)))


def test_generates_unique_id() -> None:
    use_case, _, _ = make_use_case()
    r1 = use_case.execute(valid_command())
    r2 = use_case.execute(valid_command())
    assert r1.id != r2.id
    assert isinstance(r1.id, UUID)


def test_saves_file_and_metadata() -> None:
    use_case, repo, storage = make_use_case()
    result = use_case.execute(valid_command())
    storage.save.assert_called_once()
    repo.save.assert_called_once()
    assert result.uploaded_by is None


def test_rolls_back_storage_on_db_failure() -> None:
    use_case, repo, storage = make_use_case()
    repo.save.side_effect = RuntimeError("DB error")
    with pytest.raises(RuntimeError):
        use_case.execute(valid_command())
    storage.delete.assert_called_once()


def test_upload_with_categoria() -> None:
    use_case, _, _ = make_use_case()
    result = use_case.execute(valid_command(categoria="empresa"))
    assert result.categoria == "empresa"


def test_upload_without_categoria_defaults_null() -> None:
    use_case, _, _ = make_use_case()
    result = use_case.execute(valid_command(categoria=None))
    assert result.categoria is None


def test_upload_invalid_categoria_returns_422() -> None:
    use_case, _, _ = make_use_case()
    with pytest.raises(InvalidDocumentCategory):
        use_case.execute(valid_command(categoria="invalida"))
