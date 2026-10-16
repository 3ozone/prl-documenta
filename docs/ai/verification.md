# Verificación

> Estrategia de tests del proyecto. Este documento es para la IA.
> La versión humana está en `docs/guia-diseno-aplicaciones.md` (paso 10).

---

## Regla de oro

El agente debe **demostrar** que algo funciona, no solo afirmarlo.
No se marca un módulo como `done` sin tests que pasen.

## Enfoque: solo tests de integración + TDD

Este proyecto usa **exclusivamente tests de integración** con TDD.

- No hay tests unitarios aislados.
- Cada test llama al endpoint real con una **BD de prueba** (SQLite en memoria o Postgres de test).
- Cada test se escribe **antes** de implementar el código que verifica.

### Ciclo TDD por escenario

```bash
1. Escribir test de integración (HTTP → BD)  → falla
2. Implementar endpoint, validadores, servicio → pasa
3. Refactorizar si hace falta
4. Siguiente escenario
```

La implementación se guía **por endpoint**: no se escribe un test por
validador, sino un test por escenario de la API.

## Qué debe cubrir cada test

- **Happy path**: la operación exitosa (código 2xx + efecto en BD).
- **Error paths**: cada validación que puede fallar (código 4xx + mensaje).

Ejemplo de escenarios para el módulo de registro:

| Test | HTTP esperado |
|------|---------------|
| `test_register_success` | 201 + token |
| `test_register_missing_field` | 422 + campo faltante |
| `test_register_privacy_not_accepted` | 422 + mensaje privacidad |
| `test_register_invalid_cif` | 422 + error cif |
| `test_register_invalid_email` | 422 + error email |

## Setup de tests

- Cliente HTTP: `httpx.AsyncClient`.
- BD de prueba: aislada por test (fixture con rollback o BD en memoria).
- Configuración: `pytest` con `asyncio_mode = auto`.
- Las dependencias externas (BD real, LDAP) se sustituyen por fakes en los tests.

## Cuándo se considera terminado

- Todos los tests pasan (`pytest` en verde).
- Cada `R<n>` tiene al menos un test que lo verifica.
- El checklist de calidad del `design.md` está completo.
