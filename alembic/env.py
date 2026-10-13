"""Entorno Alembic: usa DATABASE_URL del entorno y Base.metadata de models."""

import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.infrastructure.persistence.database import Base

# TODO: importar models para registrar las tablas en Base.metadata.
# from app.infrastructure.persistence import models  # noqa: F401

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# URL por variable de entorno (default: PostgreSQL del docker-compose).
config.set_main_option(
    "sqlalchemy.url",
    os.getenv("DATABASE_URL", "postgresql+psycopg://kenko:kenko@localhost:5432/kenko_documents"),
)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Migraciones sin conexión (genera SQL)."""
    context.configure(url=config.get_main_option("sqlalchemy.url"), target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Migraciones con conexión."""
    connectable = engine_from_config(config.get_section(config.config_ini_section, {}), prefix="sqlalchemy.", poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
