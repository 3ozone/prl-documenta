# ── Build stage ────────────────────────────────────────────────────────────────
FROM python:3.13-slim AS builder

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY backend/pyproject.toml backend/uv.lock ./

# Install dependencies into /app/.venv (no dev deps)
RUN uv sync --frozen --no-dev

# ── Runtime stage ───────────────────────────────────────────────────────────────
FROM python:3.13-slim AS runtime

WORKDIR /app

# Copy virtualenv from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application source
COPY backend/src ./src

# Storage directory for uploaded files
RUN mkdir -p /app/storage

# Environment defaults (override at runtime)
ENV PYTHONPATH=/app/src \
    DATABASE_URL="sqlite:///./prl_documenta.db" \
    JWT_SECRET_KEY="change-me-in-production" \
    DEFAULT_ADMIN_PASSWORD="admin123" \
    STORAGE_ROOT="/app/storage" \
    PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
