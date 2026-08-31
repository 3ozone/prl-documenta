# Requirements — core_download (Descarga de documentos)

> Notación EARS estricta. Cada requirement es verificable por al menos un test.

---

## R1

CUANDO un cliente autenticado envía una petición `GET /api/v1/documents/{document_id}/download`, el sistema DEBE devolver HTTP 200 con el cuerpo del fichero PDF en formato original y el header `Content-Type: application/pdf`.

## R2

CUANDO un cliente autenticado envía una petición `GET /api/v1/documents/{document_id}/download` y el `document_id` no existe en la base de datos, el sistema DEBE devolver HTTP 404 con un mensaje de error que indique que el documento no fue encontrado.

## R3

CUANDO un cliente autenticado envía una petición `GET /api/v1/documents/{document_id}/download` y el documento existe pero `deleted_at` no es nulo, el sistema DEBE devolver HTTP 404 con el mismo mensaje que para documento inexistente.

## R4

CUANDO un cliente no autenticado envía una petición `GET /api/v1/documents/{document_id}/download`, el sistema DEBE devolver HTTP 401.

> **Nota de implementación:** La feature `auth` (id: 9) aún está pendiente. El endpoint requerirá autenticación, pero el dependency de auth se dejará como placeholder (`None`) hasta que `auth` esté implementada. Una vez `auth` disponible, el router invocará el dependency real de sesión.

## R5

CUANDO el sistema devuelve HTTP 200 para `GET /api/v1/documents/{document_id}/download`, el header `Content-Disposition` DEBE incluir el nombre original del fichero en formato `attachment; filename="{nombre_archivo}"`.
