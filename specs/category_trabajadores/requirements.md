# Requirements — category_trabajadores

> EARS-strict. Cada R<n> debe ser verificable por al menos un test.

## R1
CUANDO se crea un documento con `categoria = "trabajadores"`, el sistema DEBE requerir los campos `nombre_trabajador`, `dni` y `tipo_documento` además de los campos core del documento.

## R2
CUANDO se crea un documento con `categoria = "trabajadores"` y los campos `nombre_trabajador`, `dni` o `tipo_documento` están ausentes, el sistema DEBE rechazar la petición con código HTTP 422 y un mensaje de error que identifique los campos obligatorios faltantes.

## R3
EL campo `tipo_documento` DEBE pertenecer exclusivamente al conjunto `formacion`, `reconocimiento_medico`, `entrega_epi`, `aptitud_medica`. CUALQUIER otro valor DEBE producir un error 422.

## R4
LOS documentos de trabajadores DEBEN almacenar los cuatro campos específicos (`nombre_trabajador`, `dni`, `puesto`, `tipo_documento`) como atributos del documento, todos persistidos en la base de datos.

## R5
CUANDO el cliente solicita `GET /api/v1/categories/trabajadores/documents` con parámetros `dni_trabajador`, `page` y `per_page`, el sistema DEBE devolver una lista paginada de documentos de trabajadores cuyo `dni` coincida con el valor solicitado.

## R6
EL listado paginado de documentos de trabajadores DEBE incluir los campos específicos de categoría (`nombre_trabajador`, `dni`, `puesto`, `tipo_documento`) en cada item devuelto.

## R7
CUANDO se solicita `GET /api/v1/categories/trabajadores/documents` sin parámetro `dni_trabajador`, el sistema DEBE devolver todos los documentos de trabajadores paginados.
