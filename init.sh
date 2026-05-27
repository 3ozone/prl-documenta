#!/usr/bin/env bash
# init.sh — Verificación e inicialización del entorno prl-documenta
#
# Este script lo ejecuta el agente al COMENZAR una sesión y antes de
# declarar cualquier tarea como `done`. Si falla, la sesión no debe avanzar.
#
# Salida esperada: códigos de salida claros y bloques marcados con [OK]/[FAIL].

set -u
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

ok()    { printf "${GREEN}[OK]${NC}    %s\n" "$1"; }
warn()  { printf "${YELLOW}[WARN]${NC}  %s\n" "$1"; }
fail()  { printf "${RED}[FAIL]${NC}  %s\n" "$1"; }

EXIT_CODE=0

echo "── 1. Verificando herramientas base ───────────────────"

# uv disponible
if ! command -v uv >/dev/null 2>&1; then
  fail "uv no está instalado (https://docs.astral.sh/uv/)"
  EXIT_CODE=1
else
  ok "uv -> $(uv --version)"
fi

# Python 3.13+
if ! command -v python3 >/dev/null 2>&1; then
  fail "python3 no está disponible"
  EXIT_CODE=1
else
  PY_OK=$(python3 -c 'import sys; print(int(sys.version_info >= (3, 13)))')
  if [ "$PY_OK" != "1" ]; then
    fail "Se requiere Python >= 3.13 (actual: $(python3 --version))"
    EXIT_CODE=1
  else
    ok "python3 -> $(python3 --version)"
  fi
fi

# Node.js disponible
if ! command -v node >/dev/null 2>&1; then
  warn "node no está instalado — pasos de frontend omitidos"
  NODE_OK=0
else
  ok "node -> $(node --version)"
  NODE_OK=1
fi

# Docker disponible
if ! command -v docker >/dev/null 2>&1; then
  warn "docker no está instalado — pasos de contenedores omitidos"
  DOCKER_OK=0
else
  ok "docker -> $(docker --version)"
  DOCKER_OK=1
fi

echo ""
echo "── 2. Verificando archivos base del arnés ─────────────"

for f in AGENTS.md feature_list.json progress/current.md \
          docs/architecture.md docs/conventions.md \
          docs/tech_stack.md docs/verification.md CHECKPOINTS.md; do
  if [ ! -f "$f" ]; then
    fail "Falta archivo base: $f"
    EXIT_CODE=1
  else
    ok "Existe $f"
  fi
done

echo ""
echo "── 3. Validando feature_list.json y specs ─────────────"

python3 - <<'PY'
import json, os, sys
try:
    data = json.load(open("feature_list.json"))
    valid = {"pending", "spec_ready", "in_progress", "done", "blocked"}
    in_progress = [f for f in data["features"] if f["status"] == "in_progress"]
    if len(in_progress) > 1:
        print(f"[FAIL]  Hay {len(in_progress)} features en in_progress (máximo 1)")
        sys.exit(1)
    requires_spec = {"spec_ready", "in_progress", "done"}
    spec_errors = []
    for f in data["features"]:
        if f["status"] not in valid:
            print(f"[FAIL]  Estado inválido en feature {f['id']}: {f['status']}")
            sys.exit(1)
        if f.get("sdd") and f["status"] in requires_spec:
            spec_dir = os.path.join("specs", f["name"])
            for fname in ("requirements.md", "design.md", "tasks.md"):
                if not os.path.isfile(os.path.join(spec_dir, fname)):
                    spec_errors.append(
                        f"feature {f['id']} ({f['name']}) en {f['status']} "
                        f"sin {spec_dir}/{fname}"
                    )
    if spec_errors:
        for e in spec_errors:
            print(f"[FAIL]  {e}")
        sys.exit(1)
    print(f"[OK]    feature_list.json válido ({len(data['features'])} features)")
    print(f"[OK]    Specs presentes para features sdd con estado no-pending")
except SystemExit:
    raise
except Exception as e:
    print(f"[FAIL]  feature_list.json o specs inválidos: {e}")
    sys.exit(1)
PY

if [ $? -ne 0 ]; then EXIT_CODE=1; fi

echo ""
echo "── 4. Entorno Python (backend/) ────────────────────────"

if [ -d "backend" ]; then
  if [ -f "backend/pyproject.toml" ]; then
    ok "backend/pyproject.toml existe"
    if command -v uv >/dev/null 2>&1; then
      (cd backend && uv sync --quiet 2>&1) && ok "uv sync completado" || { fail "uv sync falló"; EXIT_CODE=1; }
    fi
  else
    warn "backend/pyproject.toml no existe todavía"
  fi
else
  warn "Carpeta backend/ no existe todavía"
fi

echo ""
echo "── 5. Ejecutando tests Python ──────────────────────────"

if [ -d "backend/tests" ]; then
  if [ -f "backend/pyproject.toml" ] && command -v uv >/dev/null 2>&1; then
    (cd backend && uv run pytest tests/ -v 2>&1)
  else
    (cd backend && python3 -m pytest tests/ -v 2>&1)
  fi
  if [ $? -eq 0 ]; then
    ok "Tests Python pasan"
  else
    fail "Tests Python rotos"
    EXIT_CODE=1
  fi
else
  warn "Carpeta backend/tests/ no existe todavía"
fi

echo ""
echo "── 6. Entorno Node.js (frontend/) ──────────────────────"

if [ "$NODE_OK" -eq 1 ] && [ -d "frontend" ]; then
  if [ -f "frontend/package.json" ]; then
    ok "frontend/package.json existe"
    (cd frontend && npm ci --silent 2>&1) && ok "npm ci completado" || { fail "npm ci falló"; EXIT_CODE=1; }
  else
    warn "frontend/package.json no existe todavía"
  fi
else
  warn "Carpeta frontend/ no existe todavía (o node no disponible)"
fi

echo ""
echo "── 7. Ejecutando tests TypeScript ──────────────────────"

if [ "$NODE_OK" -eq 1 ] && [ -d "frontend" ] && [ -f "frontend/package.json" ]; then
  (cd frontend && npm run test --if-present 2>&1)
  if [ $? -eq 0 ]; then
    ok "Tests TypeScript pasan"
  else
    fail "Tests TypeScript rotos"
    EXIT_CODE=1
  fi
else
  warn "Tests TypeScript omitidos (frontend/ no listo)"
fi

echo ""
echo "── 8. Resumen ──────────────────────────────────────────"

if [ $EXIT_CODE -eq 0 ]; then
  ok "Entorno listo. Puedes empezar a trabajar."
else
  fail "Entorno NO está listo. Resuelve los errores antes de avanzar."
fi

exit $EXIT_CODE

