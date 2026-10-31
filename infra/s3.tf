# Bucket S3 privado para los PDFs de Documents (autorizaciones, certificados, exportaciones).
# La estructura de claves la define la aplicación (ver README); Terraform no crea objetos.
#
#   authorizations/<userId>/<authorizationId>/<timestamp>-<STATUS>.pdf
#   certificates/<userId>/<certificateId>.pdf
#   exports/<userId>/<pdfId>.pdf

resource "aws_s3_bucket" "documents_files" {
  bucket        = local.bucket_name
  force_destroy = var.force_destroy

  tags = local.common_tags
}

# ACLs desactivadas: todo el acceso se controla con políticas IAM y la bucket policy.
resource "aws_s3_bucket_ownership_controls" "documents_files" {
  bucket = aws_s3_bucket.documents_files.id

  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

# Bloqueo total de acceso público (las cuatro opciones en true).
resource "aws_s3_bucket_public_access_block" "documents_files" {
  bucket = aws_s3_bucket.documents_files.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Cifrado en reposo SSE-S3 (AES256). Sin KMS: sería sobreingeniería.
resource "aws_s3_bucket_server_side_encryption_configuration" "documents_files" {
  bucket = aws_s3_bucket.documents_files.id

  rule {
    bucket_key_enabled = true

    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Versionado desactivado: cada cambio de estado escribe una ruta nueva, nada se sobrescribe.
resource "aws_s3_bucket_versioning" "documents_files" {
  bucket = aws_s3_bucket.documents_files.id

  versioning_configuration {
    status = "Disabled"
  }
}

# Limpieza de cargas multipart incompletas a los 7 días.
# Sin expiración de objetos: la base de datos los referencia.
resource "aws_s3_bucket_lifecycle_configuration" "documents_files" {
  bucket = aws_s3_bucket.documents_files.id

  rule {
    id     = "abort-incomplete-multipart-uploads"
    status = "Enabled"

    filter {}

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }
}

# Rechaza toda petición sin TLS, sobre el bucket y sus objetos.
# depends_on evita carreras con el bloqueo de acceso público.
resource "aws_s3_bucket_policy" "documents_files" {
  bucket = aws_s3_bucket.documents_files.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "DenyInsecureTransport"
        Effect    = "Deny"
        Principal = "*"
        Action    = "s3:*"
        Resource = [
          aws_s3_bucket.documents_files.arn,
          "${aws_s3_bucket.documents_files.arn}/*",
        ]
        Condition = {
          Bool = {
            "aws:SecureTransport" = "false"
          }
        }
      }
    ]
  })

  depends_on = [aws_s3_bucket_public_access_block.documents_files]
}
