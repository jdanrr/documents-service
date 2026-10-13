"""Punto de entrada del microservicio documents.

Solo crea la app FastAPI, registra routers y delega la
composición de dependencias al composition root.
Sin lógica de negocio.
"""

from fastapi import FastAPI

from app.infrastructure.api.routers import authorizations, certificates, medical_history


def create_app() -> FastAPI:
    """Crea y configura la aplicación FastAPI."""
    # TODO: leer settings (entorno dev/prod) para título/version.
    app = FastAPI(title="kenko.documents", version="0.1.0")

    # TODO: añadir middleware de correlationId (X-Correlation-Id) si se necesita global.
    # TODO: añadir handlers de excepciones de dominio -> respuestas HTTP.

    app.include_router(authorizations.router)
    app.include_router(certificates.router)
    app.include_router(medical_history.router)

    @app.get("/health", tags=["health"])
    def health() -> dict:
        """Endpoint de salud (sin lógica, responde 200)."""
        return {"status": "ok"}

    return app


app = create_app()
