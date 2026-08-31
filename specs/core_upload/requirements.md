# Requirements — core_upload (Subida de documentos)

> Notación EARS estricta. Cada requirement es verificable por al menos un test.

---

## R1

CUANDO el cliente envía una petición `POST /api/v1/documents` con un fichero cuyo `Content-Type` no es `application/pdf` o cuya extensión no es `.pdf`, el sistema DEBE rechazar la petición con HTTP 422 y un mensaje de error que indique el formato no admitido.

## R2

CUANDO el cliente envía una petición `POST /api/v1/documents` con un fichero PDF válido y todos los campos obligatorios presentes (`nombre_archivo`, `formato`, `fecha_validez`, `fecha_caducidad`), el sistema DEBE devolver HTTP 201 con los metadatos del documento creado, incluyendo el `id` generado.

## R3

SI la petición `POST /api/v1/documents` omite cualquiera de los campos obligatorios (`nombre_archivo`, `formato`, `fecha_validez`, `fecha_caducidad`) ENTONCES el sistema DEBE rechazar la petición con HTTP 422 e indicar en el cuerpo de respuesta qué campo o campos faltan.

## R4

CUANDO el sistema procesa una subida de documento válida, el sistema DEBE generar un identificador único (`id`) de tipo UUID v4 para cada documento, garantizando que no colisiona con ningún `id` existente en la base de datos.

## R5

SI `fecha_caducidad` es igual o anterior a `fecha_validez` ENTONCES el sistema DEBE rechazar la petición con HTTP 422 y un mensaje de error que especifique que `fecha_caducidad` debe ser posterior a `fecha_validez`.

## R6

CUANDO el sistema acepta un documento válido, el sistema DEBE persistir el fichero PDF en el almacenamiento de ficheros (volumen Docker local en MVP) en una ruta determinista derivada del `id` del documento.

## R7

CUANDO el sistema acepta un documento válido, el sistema DEBE persistir los metadatos (`id`, `nombre_archivo`, `formato`, `fecha_validez`, `fecha_caducidad`) en la base de datos MariaDB de forma atómica junto con la escritura del fichero: si falla cualquiera de las dos operaciones, el sistema DEBE revertir ambas.

## R8

SI ocurre un error inesperado durante la persistencia (base de datos o almacenamiento) ENTONCES el sistema DEBE devolver HTTP 500, registrar el error con nivel `ERROR` en el logger de infraestructura (incluyendo `request_id`) y NO exponer stack traces al cliente.

## R9

El sistema DEBE aceptar únicamente el valor `"pdf"` para el campo `formato`; cualquier otro valor DEBE ser rechazado con HTTP 422.

## R10

CUANDO el cliente envía una petición válida, el sistema DEBE aceptar el campo opcional `categoria` con uno de los valores permitidos (`"empresa"`, `"trabajadores"`, `"equipos"`); si se omite, el sistema DEBE almacenarlo como nulo. Si se envía un valor distinto a los permitidos, el sistema DEBE rechazar la petición con HTTP 422.

## R11

CUANDO el sistema acepta un documento válido, el sistema DEBE almacenar el campo `uploaded_by` (UUID del usuario que sube el documento); si no hay sesión autenticada, DEBE almacenarlo como nulo.
