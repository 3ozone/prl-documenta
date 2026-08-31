# Requirements — frontend_categories

> Notación EARS estricta. Cada requirement cubre al menos un criterio de
> aceptación del `feature_list.json` id 14.

---

## R1

El sistema DEBE renderizar la página `/categories/empresa` como Server
Component, filtrando en cliente los documentos cuya `categoria` sea
`"empresa"` a partir de la respuesta de `GET /api/v1/documents`.

---

## R2

El sistema DEBE renderizar la página `/categories/trabajadores` como
Server Component, filtrando en cliente los documentos cuya `categoria`
sea `"trabajadores"` a partir de la respuesta de `GET /api/v1/documents`.

---

## R3

El sistema DEBE renderizar la página `/categories/equipos` como Server
Component, filtrando en cliente los documentos cuya `categoria` sea
`"equipos"` a partir de la respuesta de `GET /api/v1/documents`.

---

## R4

CUANDO la página `/categories/empresa` se carga, el sistema DEBE mostrar
únicamente los documentos con `categoria === "empresa"` en la tabla
de listado. Documentos de otras categorías NO DEBEN aparecer.

---

## R5

CUANDO la página `/categories/trabajadores` se carga, el sistema DEBE
mostrar únicamente los documentos con `categoria === "trabajadores"` en
la tabla de listado. Documentos de otras categorías NO DEBEN aparecer.

---

## R6

CUANDO la página `/categories/equipos` se carga, el sistema DEBE mostrar
únicamente los documentos con `categoria === "equipos"` en la tabla de
listado. Documentos de otras categorías NO DEBEN aparecer.

---

## R7

MIENTRAS el usuario autenticado tiene rol `viewer`, el sistema DEBE
ocultar el botón "Subir documento" en las páginas de categoría
`/categories/empresa`, `/categories/trabajadores` y `/categories/equipos`.

---

## R8

MIENTRAS el usuario autenticado tiene rol `admin`, el sistema DEBE
mostrar el botón "Subir documento" en las páginas de categoría, enlazando
a `/categories/<slug>/upload` correspondiente.

---

## R9

El sistema DEBE proteger las rutas `/categories/*/upload` de forma que
solo usuarios con rol `admin` puedan acceder; un `viewer` que navegue a
cualquiera de esas URLs DEBE ser redirigido a `/categories/<slug>`.

---

## R10

CUANDO el admin accede a `/categories/empresa/upload`, el sistema DEBE
mostrar un formulario con los campos obligatorios comunes
(`nombre_archivo`, `fecha_validez`, `fecha_caducidad`, `file`) más los
campos específicos de empresa: `razon_social` (texto), `cif` (texto),
`actividad_economica` (texto), `centro_trabajo` (texto).

---

## R11

CUANDO el admin accede a `/categories/trabajadores/upload`, el sistema
DEBE mostrar un formulario con los campos obligatorios comunes más los
campos específicos de trabajador: `nombre_trabajador` (texto), `dni`
(texto), `puesto` (texto), `tipo_documento` (select con valores:
`formacion`, `reconocimiento_medico`, `entrega_epi`, `aptitud_medica`).

---

## R12

CUANDO el admin accede a `/categories/equipos/upload`, el sistema DEBE
mostrar un formulario con los campos obligatorios comunes más los campos
base de equipo: `id_equipo` (texto), `nombre_equipo` (texto),
`numero_serie` (texto), `ubicacion` (texto) y un select `subtipo` con
valores `mantenimiento` e `inspeccion`.

---

## R13

MIENTRAS el usuario está rellenando el formulario `/categories/equipos/upload`
y el campo `subtipo` tiene el valor `mantenimiento`, el sistema DEBE
mostrar los campos adicionales: `tipo_mantenimiento` (texto),
`empresa_mantenedora` (texto), `fecha_proximo_mantenimiento` (fecha).

---

## R14

MIENTRAS el usuario está rellenando el formulario `/categories/equipos/upload`
y el campo `subtipo` tiene el valor `inspeccion`, el sistema DEBE mostrar
los campos adicionales: `organismo_inspector` (texto),
`resultado_inspeccion` (texto), `fecha_proxima_inspeccion` (fecha).

---

## R15

CUANDO el usuario intenta enviar cualquier formulario de categoría con un
campo obligatorio vacío, el sistema DEBE rechazarlo en cliente mostrando
el mensaje de error correspondiente por campo, sin realizar ninguna
petición HTTP.

---

## R16

CUANDO el usuario intenta enviar cualquier formulario de categoría con un
archivo que no es PDF, el sistema DEBE rechazarlo en cliente (antes de la
petición HTTP) mostrando el mensaje `"Solo se permiten archivos PDF"`.

---

## R17

CUANDO el formulario de subida de cualquier categoría es válido en
cliente y el usuario lo envía, el sistema DEBE llamar al Route Handler
`POST /api/documents/upload` incluyendo todos los campos específicos de
la categoría como campos adicionales del `FormData`, junto con el campo
`categoria` con el valor correspondiente al slug.

---

## R18

CUANDO `POST /api/documents/upload` responde con `201`, el sistema DEBE
redirigir al usuario a `/categories/<slug>` y mostrar un mensaje de
éxito.

---

## R19

SI `POST /api/documents/upload` responde con un código de error (4xx/5xx)
ENTONCES el sistema DEBE mostrar el mensaje de error recibido del backend
sin redirigir al usuario fuera del formulario de categoría.

---

## R20

El sistema DEBE exportar los tipos TypeScript `UploadEmpresaFormValues`,
`UploadTrabajadorFormValues` y `UploadEquipoFormValues` en
`frontend/src/lib/types.ts`, cada uno extendiendo los campos comunes de
subida con los campos específicos de su categoría.
