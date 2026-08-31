# Requirements — category_equipos

> EARS-strict. Cada R<n> debe ser verificable por al menos un test.

## R1
CUANDO se crea un documento con `categoria = "equipos"`, el sistema DEBE requerir los campos `id_equipo` y `nombre_equipo` además de los campos core del documento.

## R2
CUANDO se crea un documento con `categoria = "equipos"` y los campos `id_equipo` o `nombre_equipo` están ausentes, el sistema DEBE rechazar la petición con código HTTP 422 y un mensaje de error que identifique los campos obligatorios faltantes.

## R3
CUANDO se crea un documento con `categoria = "equipos"` y `subtipo = "mantenimiento"`, el sistema DEBE requerir los campos `tipo_mantenimiento`, `empresa_mantenedora` y `fecha_proximo_mantenimiento`.

## R4
CUANDO se crea un documento con `categoria = "equipos"` y `subtipo = "mantenimiento"` con cualquiera de los campos `tipo_mantenimiento`, `empresa_mantenedora` o `fecha_proximo_mantenimiento` ausentes, el sistema DEBE rechazar la petición con código HTTP 422.

## R5
CUANDO se crea un documento con `categoria = "equipos"` y `subtipo = "inspeccion"`, el sistema DEBE requerir los campos `organismo_inspector`, `resultado_inspeccion` y `fecha_proxima_inspeccion`.

## R6
CUANDO se crea un documento con `categoria = "equipos"` y `subtipo = "inspeccion"` con cualquiera de los campos `organismo_inspector`, `resultado_inspeccion` o `fecha_proxima_inspeccion` ausentes, el sistema DEBE rechazar la petición con código HTTP 422.

## R7
LOS documentos de equipos DEBEN almacenar los cuatro campos base (`id_equipo`, `nombre_equipo`, `numero_serie`, `ubicacion`) y los campos conditionally-required según el subtipo, todos persistidos en la base de datos.

## R8
CUANDO el cliente solicita `GET /api/v1/categories/equipos/documents` con el parámetro `id_equipo`, el sistema DEBE devolver una lista paginada de documentos de equipos cuyo `id_equipo` coincida con el valor solicitado.

## R9
EL listado paginado de documentos de equipos DEBE incluir todos los campos específicos de categoría en cada item devuelto, incluyendo los campos del subtipo cuando estén presentes.

## R10
CUANDO se solicita `GET /api/v1/categories/equipos/documents` sin parámetro `id_equipo`, el sistema DEBE devolver todos los documentos de equipos paginados.