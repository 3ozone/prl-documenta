# Requirements — frontend_reports

> Feature id: 16 | Notación EARS estricta | Vinculado a `feature_list.json` acceptance criteria.

---

## R1

El sistema DEBE renderizar la página `/reports` únicamente dentro del grupo de
rutas autenticadas `(dashboard)`, de modo que el middleware de Next.js la
proteja con la cookie `token` httpOnly.

_Verifica el acceptance: "Solo usuarios autenticados pueden generar informes"._

---

## R2

CUANDO un usuario no autenticado (sin cookie `token` válida) intenta acceder a
`/reports`, el sistema DEBE redirigir a `/login` sin mostrar el contenido de la
página.

_Verifica el acceptance: "Solo usuarios autenticados pueden generar informes"._

---

## R3

El sistema DEBE mostrar en `/reports` un selector de formato con exactamente
dos opciones: `CSV` y `PDF`. El valor por defecto DEBE ser `CSV`.

_Verifica el acceptance: "Selector de formato (CSV / PDF)"._

---

## R4

El sistema DEBE mostrar en `/reports` un selector de categoría con cuatro
opciones: `todas`, `empresa`, `trabajadores` y `equipos`. El valor por defecto
DEBE ser `todas`.

_Verifica el acceptance: "Selector de categoría opcional (empresa, trabajadores,
equipos, todas)"._

---

## R5

CUANDO el usuario hace clic en el botón "Generar informe", el sistema DEBE
deshabilitar el botón y mostrar un indicador de carga visible (spinner o texto
"Generando…") mientras la petición al proxy está en curso.

_Verifica el acceptance: "Durante la descarga se muestra un estado de carga"._

---

## R6

CUANDO el usuario hace clic en el botón "Generar informe", el sistema DEBE
enviar una petición `GET` al Route Handler `/api/proxy/reports` con los query
params `formato` y `categoria` reflejando los valores seleccionados en el
formulario.

_Verifica el acceptance: "Botón 'Generar informe' descarga el archivo directamente"._

---

## R7

El sistema DEBE implementar el Route Handler
`frontend/src/app/api/proxy/reports/route.ts` que, al recibir la petición
`GET /api/proxy/reports`, lea la cookie `token` httpOnly desde las cabeceras
del servidor y reenvíe la petición a `GET /reports?formato=...&categoria=...`
del backend FastAPI incluyendo el token en la cabecera `Authorization: Bearer`.

_Verifica el acceptance: "Solo usuarios autenticados pueden generar informes"
(el token nunca pasa al cliente)._

---

## R8

CUANDO el backend responde con código `200` y un cuerpo binario (CSV o PDF),
el Route Handler DEBE retransmitir la respuesta al cliente conservando las
cabeceras `Content-Type` y `Content-Disposition` originales del backend.

_Verifica el acceptance: "Botón 'Generar informe' descarga el archivo directamente"._

---

## R9

CUANDO el cliente recibe el blob del Route Handler con código `200`, el sistema
DEBE crear un `object URL` a partir del blob, inyectar un elemento `<a download>`
en el DOM con ese URL y disparar su click programático para iniciar la descarga
del archivo en el navegador del usuario.

_Verifica el acceptance: "Botón 'Generar informe' descarga el archivo directamente"._

---

## R10

CUANDO la petición al Route Handler finaliza (ya sea con éxito o error), el
sistema DEBE eliminar el indicador de carga y volver a habilitar el botón
"Generar informe".

_Verifica el acceptance: "Durante la descarga se muestra un estado de carga"._

---

## R11

SI el Route Handler recibe del backend un código de estado `401` o `403`,
ENTONCES el sistema DEBE devolver ese mismo código al cliente y el componente
DEBE mostrar un mensaje de error "No tienes permiso para generar informes."

_Verifica el acceptance: "Solo usuarios autenticados pueden generar informes"._

---

## R12

SI el Route Handler recibe del backend un código de estado distinto de `200`,
`401` y `403` (p. ej. `500`, `503`), ENTONCES el sistema DEBE devolver código
`502` al cliente y el componente DEBE mostrar un mensaje de error "Error al
generar el informe. Inténtalo de nuevo."

_Verifica el acceptance: "Botón 'Generar informe' descarga el archivo directamente"
(flujo de error visible al usuario)._
