"""Integration tests for POST /api/v1/documents."""
import io


def _pdf_file(filename: str = "test.pdf"):
    return ("file", (filename, io.BytesIO(b"%PDF-1.4 test"), "application/pdf"))


def _form_data(**kwargs):
    defaults = {
        "nombre_archivo": "test_doc",
        "formato": "pdf",
        "fecha_validez": "2025-01-01",
        "fecha_caducidad": "2025-12-31",
    }
    defaults.update(kwargs)
    return defaults


def test_upload_success_returns_201(client) -> None:
    resp = client.post(
        "/api/v1/documents",
        data=_form_data(),
        files=[_pdf_file()],
    )
    assert resp.status_code == 201
    body = resp.json()
    assert "id" in body
    assert body["nombre_archivo"] == "test_doc"
    assert body["formato"] == "pdf"


def test_upload_missing_field_returns_422(client) -> None:
    # Missing nombre_archivo
    resp = client.post(
        "/api/v1/documents",
        data={"formato": "pdf", "fecha_validez": "2025-01-01", "fecha_caducidad": "2025-12-31"},
        files=[_pdf_file()],
    )
    assert resp.status_code == 422


def test_upload_non_pdf_returns_422(client) -> None:
    resp = client.post(
        "/api/v1/documents",
        data=_form_data(),
        files=[("file", ("test.txt", io.BytesIO(b"not pdf"), "text/plain"))],
    )
    assert resp.status_code == 422


def test_upload_invalid_expiry_returns_422(client) -> None:
    resp = client.post(
        "/api/v1/documents",
        data=_form_data(fecha_validez="2025-12-31", fecha_caducidad="2025-01-01"),
        files=[_pdf_file()],
    )
    assert resp.status_code == 422


def test_upload_invalid_formato_returns_422(client) -> None:
    resp = client.post(
        "/api/v1/documents",
        data=_form_data(formato="docx"),
        files=[_pdf_file()],
    )
    assert resp.status_code == 422


def test_upload_returns_500_on_unexpected_persistence_error(client, monkeypatch) -> None:
    """R8: errores inesperados de persistencia devuelven HTTP 500."""
    from application.use_cases.upload_document import UploadDocumentUseCase

    def boom(self, command):
        raise RuntimeError("DB exploded")

    monkeypatch.setattr(UploadDocumentUseCase, "execute", boom)

    resp = client.post(
        "/api/v1/documents",
        data=_form_data(),
        files=[_pdf_file()],
    )
    assert resp.status_code == 500
    assert "RuntimeError" not in resp.text
    assert "traceback" not in resp.text.lower()
