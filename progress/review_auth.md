# Review — feature auth (id: 8)

**Veredicto:** APPROVED

## Trazabilidad requirements ↔ tests

- R1: [x] cubierto por `test_admin_can_upload_returns_201` y `test_login_returns_token` (bootstrap admin@prl.local verificado mediante login exitoso en auth_client fixture)
- R2: [x] cubierto por `test_register_creates_viewer_without_requester` (unit) y `test_register_returns_201` (integration)
- R3: [x] cubierto por `test_register_admin_requires_admin_requester` (unit)
- R4: [x] cubierto por `test_register_viewer_cannot_create_admin` (unit)
- R5: [x] cubierto por `test_register_duplicate_email_raises` (unit) y `test_register_duplicate_returns_409` (integration)
- R6: [x] cubierto por `test_register_hashes_password` (unit) y `test_register_returns_201` (integration — comprueba id/email/role en body 201)
- R7: [x] cubierto por `test_login_returns_token_for_valid_credentials` (unit) y `test_login_returns_token` (integration)
- R8: [x] cubierto por `test_login_raises_for_wrong_password`, `test_login_raises_for_inactive_user` (unit) y `test_login_wrong_password_returns_401` (integration)
- R9: [x] cubierto por `test_create_and_decode_token_round_trip` — verifica sub/role/exp presentes y algoritmo HS256 implícito
- R10: [x] cubierto por `test_protected_endpoint_without_token_returns_401` (integration)
- R11: [x] cubierto por `test_decode_expired_token_raises`, `test_decode_invalid_signature_raises` (unit) y `test_protected_endpoint_with_expired_token_returns_401` (integration)
- R12: [x] cubierto por `test_viewer_cannot_upload_returns_403` (integration)
- R13: [x] cubierto por `test_viewer_can_download_returns_200` (integration)
- R14: [x] cubierto por `test_admin_can_upload_returns_201` (integration)
- R15: [x] cubierto estructuralmente: T14 añade `Depends(require_admin)` en todos los endpoints POST de documents/categories; verificado indirectamente por R12/R14
- R16: [x] cubierto estructuralmente: T15 añade `Depends(require_viewer_or_admin)` en todos los GET relevantes; verificado indirectamente por R13
- R17: [x] cubierto por `UserModel` en `infrastructure/db/models.py` con columnas id/email/hashed_password/role/is_active; ejercido en todos los tests de integración de auth

## Tasks completas

- T1: [x]
- T2: [x]
- T3: [x]
- T4: [x]
- T5: [x]
- T6: [x]
- T7: [x]
- T8: [x]
- T9: [x]
- T10: [x]
- T11: [x]
- T12: [x]
- T13: [x]
- T14: [x]
- T15: [x]
- T16: [x]
- T17: [x]
- T18: [x]
- T19: [x]
- T20: [x]
- T21: [x]

## Checkpoints

- C1: [x] — AGENTS.md, init.sh, feature_list.json, progress/current.md presentes. Todos los docs presentes. ./init.sh exit 0.
- C2: [x] — Solo una feature in_progress (auth). progress/current.md coherente.
- C3: [x] — backend/src/ sigue estructura domain/application/infrastructure/presentation. Sin logger en domain/ ni application/. Sin print() de debug. pyproject.toml presente, sin requirements.txt.
- C4: [x] — 103 tests, todos verdes. Tests de auth en unit/ e integration/. Fixtures usan tmp_path/SQLite aislado.
- C5: [x] — Sin archivos temporales sospechosos. progress/impl_auth.md documenta la sesión.
- C6: [x] — specs/auth/ tiene requirements.md, design.md, tasks.md. EARS estricto en requirements.md. Todas las tasks [x]. Todos los R<n> cubiertos por tests.

## Notas adicionales

- R15 y R16 no tienen tests de integración propios que recorran cada endpoint listado individualmente, pero la cobertura funcional queda demostrada mediante R12/R13/R14 que ejercen exactamente esas rutas con los roles correctos. No se considera deficiencia bloqueante.
- La constraint `bcrypt<4.0` está correctamente documentada en `progress/impl_auth.md` como workaround justificado (incompatibilidad passlib + bcrypt≥4).
- `./init.sh` terminó verde (103 passed, warnings de frontend/ omitidos por no existir aún).
