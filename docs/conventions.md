# Convenciones de código

> Homogeneidad extrema. La IA predice mejor cuando el repositorio se parece
> a sí mismo en todas partes.

## Gestión de dependencias y entorno

### Python

- **Gestor:** `pyproject.toml` + `uv`. Nunca `requirements.txt`.
- **Entorno virtual:** `.venv` en la raíz de `backend/`, creado con `uv venv`.
- **Instalar dependencias:** `uv sync` (no `pip install`).
- **Añadir una dependencia:** `uv add <paquete>` (actualiza `pyproject.toml` y el lockfile).
- **Añadir dependencia de desarrollo:** `uv add --dev <paquete>`.

```bash
# Arranque del entorno backend
cd backend
uv venv
uv sync
```

### TypeScript

- **Gestor:** `npm` con `package.json` y `package-lock.json`. Nunca `yarn` ni `pnpm`.
- **Instalar dependencias:** `npm ci` en CI, `npm install` en desarrollo.

## Estilo Python

- **Versión:** Python 3.13+ (sintaxis `list[str]`, `type X = ...` permitidos).
- **Formato:** Ruff (PEP 8 estricto). Líneas máximo 100 caracteres.
- **Imports:** stdlib primero, luego third-party, luego locales. Una línea por módulo.
- **Strings:** comillas dobles `"..."` siempre. Comillas simples solo
  para escapar comillas dobles dentro.
- **f-strings** para interpolación. Nada de `.format()` ni `%`.

## Estilo TypeScript

- **Versión:** TypeScript 5.x con `strict: true`.
- **Formato:** Prettier (configuración por defecto). Líneas máximo 100 caracteres.
- **Imports:** con alias de path (`@/components/...`, `@/lib/...`).
- **Componentes React:** arrow functions nombradas. Nada de `export default function`.
- **Tipos:** siempre explícitos en funciones públicas. Evitar `any`.

## Nombres

### Python

| Tipo                    | Convención        | Ejemplo                  |
|-------------------------|-------------------|--------------------------|
| Módulos                 | `snake_case`      | `document_repository.py` |
| Clases                  | `PascalCase`      | `Document`               |
| Funciones / variables   | `snake_case`      | `upload_document`        |
| Constantes              | `UPPER_SNAKE`     | `MAX_FILE_SIZE_MB`       |
| Privadas                | prefijo `_`       | `_validate_expiry`       |

### TypeScript

| Tipo                    | Convención        | Ejemplo                  |
|-------------------------|-------------------|--------------------------|
| Archivos componente     | `PascalCase`      | `DocumentCard.tsx`       |
| Archivos utilidad       | `camelCase`       | `formatDate.ts`          |
| Interfaces / Types      | `PascalCase`      | `DocumentMetadata`       |
| Variables / funciones   | `camelCase`       | `uploadDocument`         |
| Constantes              | `UPPER_SNAKE`     | `MAX_FILE_SIZE_MB`       |

## Estructura de archivo Python

Cada archivo en `src/` empieza con:

```python
"""Una línea describiendo el propósito del módulo."""
from __future__ import annotations

# imports stdlib
import os
from datetime import date

# imports third-party
import structlog
from sqlalchemy.orm import Session

# imports locales
from src.domain.document import Document
```

## Tests

### Python (pytest)

- Un archivo de test por módulo: `tests/test_<módulo>.py`.
- Funciones sueltas `test_<descripción>`, sin clases salvo que el contexto
  lo justifique.
- Cada test usa `tmp_path` (fixture de pytest) o `tempfile.TemporaryDirectory()`.
- Nombres descriptivos: `test_upload_rejects_non_pdf_file`.

### TypeScript (Vitest)

- Un archivo de test por módulo: `<módulo>.test.ts`.
- `describe` + `it` para agrupar por unidad lógica.
- Nombres descriptivos: `it("rejects upload when expiry is before start date")`.

## Manejo de errores

Excepciones del dominio en `src/domain/exceptions.py`:

```python
class PrlError(Exception):
    """Base para errores del dominio PRL."""

class DocumentNotFound(PrlError):
    """Se lanza cuando se busca un documento inexistente."""

class InvalidExpiryDate(PrlError):
    """Se lanza cuando fecha_caducidad <= fecha_validez."""
```

La capa de presentación (FastAPI) captura excepciones del dominio y las
transforma en respuestas HTTP con el código de estado apropiado. Nunca
propaga stack traces al cliente.

## Logging

### Python — logging (stdlib)

```python
import logging

log = logging.getLogger(__name__)

# Uso correcto: mensaje + contexto estructurado con extra={}
log.info("document.uploaded", extra={"document_id": doc.id, "user_id": user.id})
log.warning("document.expiry_soon", extra={"document_id": doc.id, "days_left": 12})
log.error("document.upload_failed", extra={"filename": filename}, exc_info=True)
```

- **Nivel mínimo en producción:** `INFO`.
- **Nivel en desarrollo:** `DEBUG`.
- **Formato:** JSON en producción via `JsonFormatter` (configurado en `infrastructure/logging.py`). Texto en desarrollo.
- El logger **nunca** se instancia en `domain/`. Solo en `infrastructure/` y `presentation/`.
- No usar `print()` en ningún caso.

### TypeScript — console

```typescript
// lib/logger.ts — wrapper centralizado
const log = {
  info:  (data: Record<string, unknown>, event: string) => console.log(JSON.stringify({ level: "info",  event, ...data })),
  warn:  (data: Record<string, unknown>, event: string) => console.warn(JSON.stringify({ level: "warn",  event, ...data })),
  error: (data: Record<string, unknown>, event: string) => console.error(JSON.stringify({ level: "error", event, ...data })),
}

// Uso correcto
log.info({ documentId, userId }, "document.uploaded")
log.warn({ documentId, daysLeft }, "document.expiry_soon")
log.error({ err: err.message, filename }, "document.upload_failed")
```

- **Formato:** JSON estructurado siempre, tanto en producción como en desarrollo.
- Los componentes React no importan `console` directamente. Todo el logging
  del frontend se centraliza en `lib/logger.ts`.
- Sin dependencias externas.

## Comentarios

Por defecto **no** se escriben. Solo se permiten cuando explican un *por qué*
no obvio (p. ej. workaround documentado, invariante sutil). Los nombres deben
hacer el resto.
