# Bus de eventos compartido: es único y ya existe. Aquí solo se referencia.
# Nombre derivado de variables: {project}-{environment}-bus (kenko-dev-bus / kenko-prod-bus).

data "aws_cloudwatch_event_bus" "shared" {
  name = "${var.project}-${var.environment}-bus"
}

# Datos auxiliares para construir ARNs sin hardcodear cuentas ni regiones.
data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

locals {
  # Nombres según convención: {proyecto}-{entorno}-documents-profile[-dlq]
  # y regla {proyecto}-{entorno}-profile-to-documents.
  queue_name  = "${var.project}-${var.environment}-documents-profile"
  dlq_name    = "${var.project}-${var.environment}-documents-profile-dlq"
  rule_name   = "${var.project}-${var.environment}-profile-to-documents"
  bucket_name = "${var.project}-${var.environment}-documents-files"
  policy_name = "${var.project}-${var.environment}-documents-service"

  common_tags = {
    Project     = var.project
    Environment = var.environment
    Service     = "documents"
    ManagedBy   = "terraform"
  }
}
