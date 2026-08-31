# Requirements — category_empresa

> EARS-strict. Cada R<n> debe ser verificable por al menos un test.

## R1
CUANDO se crea un documento con `categoria = "empresa"`, el sistema DEBE requerir los campos `razon_social` y `cif` además de los campos core del documento.

## R2
CUANDO se crea un documento con `categoria = "empresa"` y los campos `razon_social` o `cif` están ausentes, el sistema DEBE rechazar la petición con código HTTP 422 y un mensaje de error que identifique los campos obligatorios faltantes.

## R3
LOS documentos de empresa DEBEN almacenar los cuatro campos específicos (`razon_social`, `cif`, `actividad_economica`, `centro_trabajo`) como atributos del documento, todos opcionales pero persistidos en la base de datos.

## R4
CUANDO el cliente solicita `GET /api/v1/categories/empresa/documents` con parámetros `page` y `per_page`, el sistema DEBE devolver una lista paginada de documentos cuya `categoria` sea "empresa".

## R5
EL listado paginado de documentos de empresa DEBE incluir los campos específicos de categoría en cada item devuelto.

## R6
CUANDO se filtra por parámetro `estado` en `GET /api/v1/categories/empresa/documents`, el sistema DEBE devolver únicamente los documentos de empresa cuyo estado calculado sea igual al valor solicitado (`vigente` | `caducada`).

## R7
EL estado de un documento de empresa DEBE calcularse como `vigente` cuando `fecha_caducidad` es posterior a la fecha actual, y como `caducada` cuando `fecha_caducidad` es anterior o igual a la fecha actual.