# Versiones de Terraform y provider AWS.
# Estado local por ahora; bloque backend S3 comentado como referencia (no activarlo).

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Referencia futura (NO activar por ahora):
  # backend "s3" {
  #   bucket = "kenko-terraform-state"
  #   key    = "documents/messaging.tfstate"
  #   region = "us-east-1"
  # }
}

# Región tomada de la variable environment (ver variables.tf).
provider "aws" {
  region = var.aws_region
}
