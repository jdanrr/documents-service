"""Adaptador de almacenamiento de PDFs en S3 (boto3)."""

import boto3

from app.application.errors import StorageError
from app.application.ports.output.pdf_storage_ports import DocumentStoragePort
from app.infrastructure.config.settings import Settings


class S3DocumentStorage(DocumentStoragePort):
    """Guarda PDFs en S3 y retorna la key como referencia."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client = boto3.client("s3", region_name=settings.aws_region)

    async def save(
        self, key: str, content: bytes, content_type: str = "application/pdf"
    ) -> str:
        """Sube el binario con la key dada (la key nunca lleva datos personales)."""
        try:
            self._client.put_object(
                Bucket=self._settings.documents_bucket_name,
                Key=key,
                Body=content,
                ContentType=content_type,
            )
        except Exception as error:
            raise StorageError("No se pudo guardar el PDF en el almacenamiento.") from error
        return key
