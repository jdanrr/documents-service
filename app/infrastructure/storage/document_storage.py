"""Adaptador de almacenamiento de PDFs (esqueleto S3 con boto3)."""

import boto3

from app.application.ports.output.pdf_storage_ports import DocumentStoragePort
from app.infrastructure.config.settings import Settings


class S3DocumentStorage(DocumentStoragePort):
    """Guarda PDFs en S3 y retorna la key como referencia."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        # TODO: self._client = boto3.client("s3", region_name=settings.aws_region)

    async def save(self, pdf_id: str, content: bytes) -> str:
        """Sube el binario al bucket y retorna la key."""
        # TODO: key = f"medical-history/{pdf_id}.pdf"
        # TODO: self._client.put_object(Bucket=self._settings.s3_bucket, Key=key, Body=content)
        # TODO: return key
        raise NotImplementedError
