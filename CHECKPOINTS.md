# CHECKPOINTS — Evaluación del estado final

> En sistemas multi-agente no se evalúa el camino, se evalúa el destino.
> Estos son los checkpoints objetivos que un juez (humano o IA) puede usar
> para decidir si el proyecto está sano.

## C1 — El arnés está completo

- [ ] Existen los archivos base: `AGENTS.md`, `init.sh`, `feature_list.json`,
      `progress/current.md`.
- [ ] Existen los docs: `docs/architecture.md`, `docs/conventions.md`,
      `docs/tech_stack.md`, `docs/verification.md`.
- [ ] `./init.sh` termina con exit code 0.

## C2 — El estado es coherente

- [ ] Como mucho una feature en `in_progress` en `feature_list.json`.
- [ ] Toda feature `done` tiene tests asociados que pasan.
- [ ] `progress/current.md` está vacío o describe la sesión activa
      (no contiene basura de sesiones anteriores).

## C3 — El código respeta la arquitectura

- [ ] `backend/src/` solo contiene los módulos previstos en
      `docs/architecture.md` (capas: `domain/`, `application/`,
      `infrastructure/`, `presentation/`).
- [ ] `frontend/src/` solo contiene los módulos previstos en
      `docs/architecture.md` (componentes, páginas, `lib/`).
- [ ] `backend/pyproject.toml` existe y declara todas las dependencias.
      No hay `requirements.txt`.
- [ ] `frontend/package.json` existe con sus dependencias declaradas.
- [ ] No hay `print()` sueltos para debug ni `console.log()` fuera de
      `lib/logger.ts`, ni TODOs sin contexto.

## C4 — La verificación es real

- [ ] `backend/tests/` tiene al menos un test por módulo de `backend/src/`.
- [ ] `frontend/` tiene tests en los componentes principales.
- [ ] Los tests de Python usan fixtures/tmpdir, no mocks frágiles de fs.
- [ ] `uv run pytest tests/ -v` (dentro de `backend/`) muestra > 0 tests
      y todos verdes.
- [ ] `npm run test` (dentro de `frontend/`) muestra > 0 tests y todos verdes.

## C5 — La sesión se cerró bien

- [ ] No hay archivos sin trackear sospechosos (`*.tmp`, `__pycache__`
      fuera del `.gitignore`).
- [ ] `progress/history.md` tiene una entrada por la última sesión.
- [ ] La última feature trabajada está reflejada en su estado correcto.

## C6 — Spec Driven Development

- [ ] Toda feature con `"sdd": true` en estado `spec_ready`, `in_progress`
      o `done` tiene su carpeta `specs/<name>/` con los 3 archivos:
      `requirements.md`, `design.md`, `tasks.md`.
- [ ] `requirements.md` usa EARS estricto (ver `docs/specs.md`).
- [ ] Toda feature `done` con `"sdd": true` tiene todas sus tasks marcadas
      `[x]` en `tasks.md`.
- [ ] Cada `R<n>` de `requirements.md` está cubierto por al menos un test
      concreto en `tests/`.

---

**Cómo usar este archivo:** el agente revisor (`.opencode/agents/reviewer.md`)
recorre cada checkbox, marca `[x]` o `[ ]`, y rechaza el cierre de sesión
si quedan boxes vacíos en C1-C6.
