"""Unit tests for DownloadDocumentUseCase."""
from datetime import date
from unittest.mock import MagicMock
from uuid import UUID

import pytest

from application.use_cases.download_document import DownloadDocumentResult, DownloadDocumentUseCase
from domain.exceptions import DocumentNotFound


def make_use_case():
    repo = MagicMock()
    storage = MagicMock()
    return DownloadDocumentUseCase(repository=repo, storage=storage), repo, storage


def test_raises_document_not_found_when_id_not_exists() -> None:
    use_case, repo, _ = make_use_case()
    doc_id = UUID("00000000-0000-0000-0000-000000000001")
    repo.get_by_id.return_value = None

    with pytest.raises(DocumentNotFound):
        use_case.execute(doc_id)


def test_raises_document_not_found_when_deleted_at_not_null() -> None:
    use_case, repo, _ = make_use_case()
    doc_id = UUID("00000000-0000-0000-0000-000000000001")
    repo.get_by_id.return_value = None

    with pytest.raises(DocumentNotFound):
        use_case.execute(doc_id)


def test_returns_content_and_filename_when_document_exists() -> None:
    use_case, repo, storage = make_use_case()
    doc_id = UUID("00000000-0000-0000-0000-000000000001")
    doc_content = b"%PDF-1.4 test content"

    mock_document = MagicMock()
    mock_document.nombre_archivo = "test_doc.pdf"
    repo.get_by_id.return_value = mock_document
    storage.read.return_value = doc_content

    result = use_case.execute(doc_id)

    assert result.content == doc_content
    assert result.nombre_archivo == "test_doc.pdf"
    repo.get_by_id.assert_called_once_with(doc_id)
    storage.read.assert_called_once_with(doc_id)
