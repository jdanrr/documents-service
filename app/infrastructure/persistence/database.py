"""Gestión de sesión SQLAlchemy (solo infraestructura).

Una sesión por request, entregada con Depends desde el composition root.
"""

from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    """Base declarativa de todos los modelos ORM."""


# TODO: crear el engine con Settings.database_url en composition y pasar la
# TODO: SessionLocal aquí (evitar variable global hardcodeada).
engine: object | None = None
SessionLocal: sessionmaker[Session] | None = None


def init_database(database_url: str) -> None:
    """Inicializa engine y SessionLocal (llamar una vez al arrancar)."""
    # TODO: create_engine(database_url, pool_pre_ping=True) + sessionmaker(bind=engine).
    raise NotImplementedError


def get_db() -> Iterator[Session]:
    """Dependencia FastAPI: entrega una sesión por request y la cierra."""
    # TODO: db = SessionLocal(); try: yield db finally: db.close().
    raise NotImplementedError
