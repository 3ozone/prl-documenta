# Tasks — Registro

> Checklist de implementación del módulo de registro.
> Enfoque TDD con **solo tests de integración**: cada test se escribe antes
> del código que verifica, agrupado por escenario.

---

## Escenario 1 — Registro exitoso (R7)

- [ ] T1 — Escribir test de integración `test_register_success` en `tests/test_register/test_register.py`. Falla (el endpoint no existe). Cubre: R7.
- [ ] T2 — Crear modelo `Company` y `User` en `register/models.py`. Cubre: R7.
- [ ] T3 — Crear schema `RegisterRequest` y `RegisterResponse` en `register/schemas.py`. Cubre: R2, R7.
- [ ] T4 — Implementar `RegisterService.register()` en `register/services.py` (hasheo bcrypt + generación JWT). Cubre: R7.
- [ ] T5 — Crear endpoint `POST /api/v1/register` en `register/router.py`. El test pasa. Cubre: R7.

## Escenario 2 — Campo obligatorio vacío (R8)

- [ ] T6 — Escribir test `test_register_missing_field`. Falla. Cubre: R8.
- [ ] T7 — Implementar validación de campos obligatorios en el endpoint. El test pasa. Cubre: R8.

## Escenario 3 — Privacidad no aceptada (R5)

- [ ] T8 — Escribir test `test_register_privacy_not_accepted`. Falla. Cubre: R5.
- [ ] T9 — Implementar `@field_validator` de `accept_privacy_policy` en `schemas.py` (exige `True`). El test pasa. Cubre: R4, R5.

## Escenario 4 — CIF inválido (R12)

- [ ] T10 — Escribir test `test_register_invalid_cif`. Falla (Pydantic no lo valida todavía). Cubre: R12.
- [ ] T11 — Implementar helper de checksum CIF/DNI en `register/validators.py` y usarlo en un `@field_validator` de `schemas.py`. El test pasa. Cubre: R12.

## Escenario 5 — Letra de DNI incorrecta (R12)

- [ ] T12 — Escribir test `test_register_invalid_dni_letter`. Falla. Cubre: R12.
- [ ] T13 — Completar la validación de DNI/NIE en el `@field_validator` de `schemas.py`. El test pasa. Cubre: R12.

## Escenario 6 — Contraseña débil (R9, R10)

- [ ] T14 — Escribir test `test_register_weak_password`. Falla. Cubre: R9, R10.
- [ ] T15 — Implementar `@field_validator` de contraseña en `schemas.py` (10+, may, min, num, especiales). El test pasa. Cubre: R9, R10.

## Escenario 7 — Teléfono inválido (R13)

- [ ] T16 — Escribir test `test_register_invalid_phone`. Falla. Cubre: R13.
- [ ] T17 — Implementar `@field_validator` de teléfono en `schemas.py` (regex fijo/móvil). El test pasa. Cubre: R13.

## Escenario 8 — Email inválido (R11)

- [ ] T18 — Escribir test `test_register_invalid_email`. Falla. Cubre: R11.
- [ ] T19 — Configurar el email como `EmailStr` en `schemas.py`. El test pasa. Cubre: R11.

## Verificación final

- [ ] T20 — Ejecutar `pytest` completo y verificar que los 8 tests pasan. Cubre: R5, R7, R8, R9, R10, R11, R12, R13, RNF1.
- [ ] T21 — Revisar checklist de calidad en `design.md`. Cubre: R1-R14.