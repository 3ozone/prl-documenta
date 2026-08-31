# Requirements — core_reporting (Generación de informes de estado documental)

> Notación EARS estricta. Cada requirement es verificable por al menos un test.

---

## R1

El sistema DEBE clasificar cada documento con `deleted_at` nulo en exactamente uno de los tres estados siguientes, usando la fecha de generación como referencia:

- **vigente**: `fecha_caducidad > fecha_referencia + 30 días`
- **proxima_a_caducar**: `fecha_referencia < fecha_caducidad <= fecha_referencia + 30 días`
- **caducada**: `fecha_caducidad <= fecha_referencia`

## R2

El sistema DEBE excluir del informe cualquier documento cuyo campo `deleted_at` no sea nulo.

## R3

DONDE el parámetro opcional `categoria` es proporcionado, el sistema DEBLE filtrar el informe para incluir únicamente los documentos cuya `categoria` coincida con el valor proporcionado.

## R4

CUANDO un cliente envía una petición `GET /api/v1/reports/status?formato=csv` y no hay errores, el sistema DEBE devolver HTTP 200 con `Content-Type: text/csv; charset=utf-8` y `Content-Disposition: attachment; filename="informe_estado_{YYYY-MM-DD_HHMMSS}.csv"`.

## R5

CUANDO un cliente envía una petición `GET /api/v1/reports/status?formato=pdf` y no hay errores, el sistema DEBE devolver HTTP 200 con `Content-Type: application/pdf`.

## R6

CUANDO el sistema genera el informe, el sistema DEBE incluir en la respuesta un campo `generated_at` con la fecha y hora exactas UTC de generación.

## R7

CUANDO un cliente envía una petición `GET /api/v1/reports/status?formato=xml` (o cualquier valor distinto de `csv` o `pdf`), el sistema DEBE devolver HTTP 400 con un mensaje de error que indique los formatos válidos.

---

## Estructura del informe CSV

El cuerpo del CSV DEBE contener las siguientes columnas en orden:

```
id,nombre_archivo,categoria,fecha_validez,fecha_caducidad,estado,dias_hasta_caducidad
```

- `estado` es el valor literal `vigente`, `proxima_a_caducar` o `caducada`
- `dias_hasta_caducidad` es un entero (negativo para caducada, cero para proxima_a_caducar, positivo para vigente)

---

## Estructura del informe PDF

El cuerpo del PDF DEBE contener:

- Título: "Informe de Estado Documental"
- Campo `generated_at` con la fecha y hora de generación
- Una tabla por cada estado posible (`vigente`, `proxima_a_caducar`, `caducada`), cada una con las columnas: `id`, `nombre_archivo`, `categoria`, `fecha_caducidad`
- Cada tabla DEBE aparecer aunque esté vacía, con la cabecera visible

---

## Notas de implementación

> **Auth (id: 9):** El endpoint requerirá autenticación en el futuro. Por ahora se deja como placeholder con un comentario `TODO`. El dependency de sesión se dejará como `None` hasta que `auth` esté implementada.