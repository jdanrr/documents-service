# Bus de eventos compartido: es único y lo creó Authentication. Aquí solo se referencia.
# Nombre derivado de variables: {project}-{environment}-bus (kenko-dev-bus / kenko-prod-bus).

data "aws_cloudwatch_event_bus" "shared" {
  name = "${var.project}-${var.environment}-bus"
}

# Datos auxiliares para construir ARNs sin hardcodear cuentas ni regiones.
data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

locals {
  # Nombres según convención: {proyecto}-{entorno}-{consumidor}-{productor}[-dlq]
  queue_name = "${var.project}-${var.environment}-notifications-documents"
  dlq_name   = "${var.project}-${var.environment}-notifications-documents-dlq"
  rule_name  = "documents-to-notifications"

  common_tags = {
    Project     = var.project
    Environment = var.environment
    Service     = "documents"
    ManagedBy   = "terraform"
  }
}
