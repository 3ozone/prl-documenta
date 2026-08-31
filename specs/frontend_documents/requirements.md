# Requirements — frontend_documents

> Notación EARS estricta. Cada requirement cubre al menos un criterio de
> aceptación del `feature_list.json` id 13.

---

## R1

El sistema DEBE renderizar la página `/documents` como Server Component,
recuperando el listado de documentos desde `GET /api/v1/documents` con el
token leído de la cookie `httpOnly` del servidor.

---

## R2

CUANDO la página `/documents` se carga, el sistema DEBE mostrar una tabla
con las columnas: `nombre_archivo`, `fecha_validez`, `fecha_caducidad`,
`estado` (badge de color) y `acciones` (botón descargar).

---

## R3

CUANDO la página `/documents` se carga, el sistema DEBE calcular el
`DocumentStatus` de cada documento usando la función `classifyStatus`
(umbral `proxima_a_caducar` ≤ 30 días, igual que en dashboard) y
renderizar el badge con los colores:
- `vigente` → verde
- `proxima_a_caducar` → amarillo
- `caducada` → rojo

---

## R4

El sistema DEBE paginar el listado de `/documents` a 20 documentos por
página usando `searchParams` de la URL (`?page=N`), sin recargar la
página completa al navegar entre páginas.

---

## R5

MIENTRAS el usuario autenticado tiene rol `viewer`, el sistema DEBE
ocultar el botón "Subir documento" en la página `/documents`.

---

## R6

MIENTRAS el usuario autenticado tiene rol `admin`, el sistema DEBE
mostrar el botón "Subir documento" en la página `/documents`, enlazando
a `/documents/upload`.

---

## R7

El sistema DEBE determinar el rol del usuario decodificando el JWT
almacenado en la cookie `httpOnly` del servidor, sin exponer el token
al cliente JavaScript.

---

## R8

El sistema DEBE proteger la ruta `/documents/upload` de forma que solo
usuarios con rol `admin` puedan acceder; un `viewer` que navegue a esa
URL DEBE ser redirigido a `/documents`.

---

## R9

CUANDO el admin accede a `/documents/upload`, el sistema DEBE mostrar un
formulario con los campos obligatorios: `nombre_archivo` (texto),
`fecha_validez` (fecha), `fecha_caducidad` (fecha) y `file` (PDF).

---

## R10

CUANDO el usuario intenta enviar el formulario de subida con un archivo
que no es PDF, el sistema DEBE rechazarlo en cliente (antes de la
petición HTTP) mostrando el mensaje `"Solo se permiten archivos PDF"`.

---

## R11

CUANDO el usuario intenta enviar el formulario de subida con algún campo
obligatorio vacío, el sistema DEBE rechazarlo en cliente mostrando el
mensaje de error correspondiente por campo.

---

## R12

CUANDO el formulario de subida es válido en cliente y el usuario lo
envía, el sistema DEBE llamar a `POST /api/v1/documents/upload`
(multipart/form-data) mediante un Route Handler de Next.js que lea el
token de la cookie `httpOnly` y añada la cabecera `Authorization: Bearer
<token>`.

---

## R13

CUANDO `POST /api/v1/documents/upload` responde con `201`, el sistema
DEBE redirigir al usuario a `/documents` y mostrar un mensaje de éxito.

---

## R14

SI `POST /api/v1/documents/upload` responde con un código de error
(4xx/5xx) ENTONCES el sistema DEBE mostrar el mensaje de error recibido
del backend sin redirigir al usuario fuera del formulario.

---

## R15

CUANDO el usuario pulsa el botón "Descargar" de un documento, el sistema
DEBE abrir el PDF en el navegador (no forzar descarga) recuperándolo a
través de un Route Handler de Next.js en `GET /api/proxy/documents/[id]/download`
que lea el token de la cookie `httpOnly` y reenvíe el stream al
navegador con `Content-Type: application/pdf`.

---

## R16

SI el Route Handler de descarga recibe un `404` del backend ENTONCES el
sistema DEBE devolver una respuesta `404` con el mensaje `"Documento no
encontrado"`.

---

## R17

CUANDO el usuario no tiene sesión válida y navega a `/documents` o
`/documents/upload`, el sistema DEBE redirigir a `/login` (ya cubierto
por `middleware.ts`, pero la página DEBE confiar en que el token existe
en cookie al renderizarse).

---

## R18

El sistema DEBE registrar en consola de servidor (usando `lib/logger.ts`)
cualquier error de red o respuesta inesperada al llamar a
`GET /api/v1/documents` o al Route Handler de descarga, incluyendo el
`document_id` afectado si aplica.
