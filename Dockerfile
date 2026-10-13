# Etapa de build: instala dependencias con uv (reproducible vía uv.lock).
FROM python:3.11-slim AS build
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
WORKDIR /app
ENV UV_SYSTEM_PYTHON=0
# Primero solo metadatos (caché de dependencias), luego el código y sync final.
COPY pyproject.toml uv.lock ./
RUN /bin/uv sync --frozen --no-dev --no-install-project
COPY app/ app/
COPY alembic/ alembic/
COPY alembic.ini ./
RUN /bin/uv sync --frozen --no-dev

# Etapa final liviana.
FROM python:3.11-slim
WORKDIR /app
# Usuario no root para ejecución.
RUN useradd --create-home --shell /bin/bash appuser
COPY --from=build --chown=appuser:appuser /app/.venv /app/.venv
COPY --from=build --chown=appuser:appuser /app/app /app/app
COPY --from=build --chown=appuser:appuser /app/alembic /app/alembic
COPY --from=build --chown=appuser:appuser /app/alembic.ini /app/alembic.ini
ENV PATH="/app/.venv/bin:$PATH"
USER appuser
EXPOSE 8000
# El compose ejecuta las migraciones antes de arrancar (ver docker-compose.yml).
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
