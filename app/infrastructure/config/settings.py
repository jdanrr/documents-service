"""Configuración por entorno con pydantic-settings (sin credenciales)."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Ajustes del servicio (dev/prod según variables de entorno)."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    env: str = "dev"
    database_url: str = "postgresql+psycopg://kenko:kenko@localhost:5432/kenko_documents"
    aws_region: str = "us-east-1"
    event_bus_name: str = "kenko-dev-bus"  # En prod: kenko-prod-bus
    notifications_rule: str = "documents-to-notifications"
    s3_bucket: str = "kenko-dev-documents"
