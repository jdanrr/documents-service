"""Gestión de sesión SQLAlchemy (solo infraestructura).

Una sesión por request, entregada con Depends desde el composition root.
"""

from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    """Base declarativa de todos los modelos ORM."""


engine: object | None = None
SessionLocal: sessionmaker[Session] | None = None


def init_database(database_url: str) -> None:
    """Inicializa engine y SessionLocal (llamar una vez al arrancar)."""
    global engine, SessionLocal
    engine = create_engine(database_url, pool_pre_ping=True)
    SessionLocal = sessionmaker(bind=engine)


def get_db() -> Iterator[Session]:
    """Dependencia FastAPI: entrega una sesión por request y la cierra."""
    if SessionLocal is None:
        raise RuntimeError("Base de datos sin inicializar: falta init_database().")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
